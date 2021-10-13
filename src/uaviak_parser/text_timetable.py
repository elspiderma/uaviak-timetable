import datetime

from uaviak_parser.exceptions import ParseTimetableError, ParseLessonError
from uaviak_parser.structures import Timetable, Lesson, TypesLesson
from utils import is_string_one_unique_char, index_upper


class TextTimetable:
    """Класс, представляющий расписание в текстовом виде.
    """
    def __init__(self, title: str, lessons: list[str]):
        """
        Args:
            title: Заголовок расписания.
            lessons: Массив уроков.
        """
        self.title = title
        self.lessons = lessons

    def _parse_lesson(self, lesson_line: str) -> Lesson:
        """
        Парсит пару из строки.

        Args:
            lesson_line: строка для парсинга

        Returns:
            Отпарсенный дата-класс расписания.

        Raises:
            ParseLessonError - ошибка парсинга строки с расписанием
        """
        # Расписание на сайте находится в следующем формате
        # {группа} {номер} [дрб] {кабинет} {фамилия_препод} {инициалы_препод} {предмет} [{тип_пары}]
        # Например:
        # 17адс1 1 дрб 214 Кольцов В.А. Учебная практика Практика
        split_line = lesson_line.split()
        types_lesson = set()

        if len(split_line) < 5:
            raise ParseLessonError(lesson_line)

        group = split_line.pop(0)  # Извлекаем группу
        try:
            number = int(split_line.pop(0))  # Извлекаем номер пары
        except ValueError:
            raise ParseLessonError(lesson_line)

        if split_line[0] == "дрб":
            types_lesson.add(TypesLesson.SPLIT)
            del split_line[0]

        # Максимальная длина кабинета 5 символов, если больше,
        # то занчит номер кабинета и фамилия преподавателя слились ("спасибо" УАвиаК за эту хуйню).
        # Примеры слияния кабинета и фамилии:
        # 18св-1 1 Св.маШабаев А.В. Учебная практика Практика
        # 19ам-2 2 дрб 410*кАпраушев И.А. Информатика
        tmp = split_line.pop(0)
        if len(tmp) <= 5:
            cabinet = tmp
            teacher = split_line.pop(0)
        else:
            # Фамилия преподавателя всегда начинает с большой буквы, соответственно ищем первую прописную букву
            # и делим строку по ней.
            try:
                index_split = index_upper(tmp[1:]) + 1  # Начинаем поиск заглавной буквы со 2 символа
            except ValueError:
                # Если мы не находим заглавную букву, то значит кабинета нет, и после него сразу идет преподаватель.
                # Например:
                # 19ом1з 1 Аминов В.Н. Выполнение работ по одной или Экзамен
                # 17п-1 1 Демонстрационный экзамен ГЭК
                cabinet = None
                teacher = tmp
            else:
                cabinet = tmp[:index_split]
                teacher = tmp[index_split:]

        # Добавляем инициалы к фамилии
        teacher += f' {split_line.pop(0)}'

        # Парсим тип пары.
        if split_line[-1] == 'Практика':
            types_lesson.add(TypesLesson.PRACTICAL)
            del split_line[-1]
        elif split_line[-1] in ('Консульт', 'Консультация'):
            types_lesson.add(TypesLesson.CONSULTATION)
            del split_line[-1]
        elif split_line[-1] == 'Экзамен':
            types_lesson.add(TypesLesson.EXAM)
            del split_line[-1]

        # Все что осталось -- предмет
        subject = ' '.join(split_line)

        return Lesson(
            number=number,
            subject=subject,
            cabinet=cabinet,
            types=types_lesson,
            group=group,
            teacher=teacher
        )

    def parse_text(self) -> Timetable:
        """
        Парсит расписание в текстовом формате.

        Returns:
            Расписание.

        Raises:
            ParseTimetableError - ошибка парсинга расписания
            ParseLessonError - ошибка парсинга строки с расписанием
        """

        # Заголовок имеет формат "Расписание преподаватели {date} {date_of_week} ({} отделение)".
        # Например:
        # Расписание 23.03.2021 Вторник (Заочное отделение)
        # или
        # Расписание на 23.03.2021 Вторник (Дневное отделение)
        split_title = self.title.split()

        if len(split_title) != 6:
            raise ParseTimetableError(self.title, self.lessons)

        date = split_title[2]

        try:
            # Парсинг даты
            day, month, year = date.split('.')
            date = datetime.date(day=int(day), month=int(month), year=int(year))
        except ValueError:
            raise ParseTimetableError(self.title, self.lessons)

        # Парсинг пар
        parsed_lesson = list()
        for i in self.lessons:
            parsed_lesson.append(self._parse_lesson(i))

        return Timetable(
            date=date,
            lessons=parsed_lesson
        )

    @classmethod
    def parse(cls, timetable: str) -> 'TextTimetable':
        """
        Разделяет заголовок, доп. информацию и пары.

        Args:
            timetable: Сырой текст расписания.
        """

        # Расписание на сайте находится в таком формате:
        #
        # <Заголовок>
        # <Доп. информация>
        # -------------------------
        # <Пара 1 для 1 преподавателя>
        # <Пара 2 для 1 преподавателя>
        # <Пара n для 1 преподавателя>
        # -------------------------
        # <Пара 1 для 2 преподавателя>
        # <Пара 2 для 2 преподавателя>
        # <Пара n для 2 преподавателя>
        # -------------------------
        # <Пара n для n преподавателя>

        timetable_lines = timetable.strip().splitlines()

        # Получаем заголовок расписания. Заголовок всегда первый.
        title = timetable_lines.pop(0)

        lesson_lines = []

        is_timetable_begin = False
        for line in timetable_lines:
            # Удаляем повторяющиеся пробелы
            line = line.strip()
            line = ' '.join(line.split())

            if line != '':  # Игнорируем пустые строки
                # Строка содержащяя только "-" является разделителем между группами
                if is_string_one_unique_char(line, '-'):
                    # Все, что идет до первого разделителя -- это различная доп. информация, которую мы игнорируем.
                    is_timetable_begin = True
                elif is_timetable_begin:
                    lesson_lines.append(line)

        return cls(title, lesson_lines)
