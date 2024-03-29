from typing import TYPE_CHECKING

from db.structures import TypesLesson
from vk_bot.core.timetable import TYPES_TO_STRING

if TYPE_CHECKING:
    from db.structures import TimetableForSomeone


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

    def _generate_lessons_line(self) -> list[str]:
        """Возвращает строку текста с парой.

        Args:
            lesson: Пара.

        Returns:
            Строка с парой.
        """
        lessons_line = list()

        for lesson in self.timetable.lessons:
            lesson_str = [f'{lesson.number})', lesson.cabinet, 'каб.', lesson.whose, lesson.subject]

            types_str = self._types_to_str(lesson.types)
            if types_str:
                lesson_str.append(types_str)

            lessons_line.append(' '.join(lesson_str))

        return lessons_line

    def _types_to_str(self, types: list[TypesLesson]):
        """Преобразует типы пары в строку.

        Args:
            types: Типы пары.

        Returns:
            Типы пар в виде строки.
        """
        def convert(t: list[TypesLesson]) -> tuple[str]:
            return tuple(TYPES_TO_STRING[i] for i in t)

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

    def generate_text_timetable(self) -> str:
        """Генерирует текст расписания.

        Returns:
            Текст расписания.
        """
        lines = list()

        lines.append(self._generate_title_line())
        lines += self._generate_lessons_line()

        lines.append('')
        lines.append(self._generate_date_line())

        return '\n'.join(lines)
