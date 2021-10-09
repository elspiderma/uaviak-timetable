from typing import TYPE_CHECKING

from db.structures import TypesLesson
from vk_bot.keyboards import generate_keyboard_date

if TYPE_CHECKING:
    import datetime
    from db.structures import TimetableForSomeone, FullLessonForSomeone
    from vk_bot.search import AbstractResult


class TimetableText:
    """Генератор расписания в тестовом формате.
    """
    def __init__(self, timetable: 'TimetableForSomeone'):
        self.timetable = timetable

    def _generate_title_line(self) -> str:
        """Возвращает заголовок текста.

        Returns:
            Заголовок теста.
        """
        return f'{self.timetable.someone.title}:'

    def _generate_lesson_line(self, lesson: 'FullLessonForSomeone'):
        """Возвращает строку текста с парой.

        Args:
            lesson: Пара.

        Returns:
            Строка с парой.
        """
        lesson_str = [f'{lesson.number})', lesson.cabinet, 'каб.', lesson.whose, lesson.subject]

        types_str = self._types_to_str(lesson.types)
        if types_str:
            lesson_str.append(types_str)

        return ' '.join(lesson_str)

    def _types_to_str(self, types: list[TypesLesson]):
        """Преобразует типы пары в строку.

        Args:
            types: Типы пары.

        Returns:
            Типы пар в виде строки.
        """
        def convert(t: list[TypesLesson]) -> tuple[str]:
            types2string = {
                TypesLesson.EXAM: 'экз',
                TypesLesson.SPLIT: 'дрб',
                TypesLesson.PRACTICAL: 'практ',
                TypesLesson.CONSULTATION: 'конс'
            }

            return tuple(types2string[i] for i in t)

        types_str = convert(types)
        if not types_str:
            return None

        return f"({', '.join(types_str)})"

    def _generate_date_line(self) -> str:
        """Возвращает строку с датой.

        Returns:
            Строка с датой.
        """
        return self.timetable.date.strftime('%a %d.%m')

    def generate_text(self) -> str:
        """Генерирует текст расписания.

        Returns:
            Текст расписания.
        """
        lines = list()

        lines.append(self._generate_title_line())
        for lesson in self.timetable.lessons:
            lines.append(self._generate_lesson_line(lesson))

        lines.append('')
        lines.append(self._generate_date_line())

        return '\n'.join(lines)


async def get_message_timetable_for_result_search(result: 'AbstractResult', date: 'datetime.date' = None) -> tuple[str, str]:
    """Возвращает текст расписания и клавиатуру с датой для результата поиска.

    Args:
        result: Результат поиска.
        date: Дата расписания, если None, то используется последняя дата.

    Returns:
        Текст расписания и клавиатура с доступными датами.
    """
    dates = await result.get_dates_timetable(9)

    # Если дата не передана, то используем последнию дату.
    if not date:
        date = dates[0]

    timetable = await result.get_timetable(date)

    kb = generate_keyboard_date(dates, date, timetable)
    message = TimetableText(timetable).generate_text()

    return message, kb.get_json()
