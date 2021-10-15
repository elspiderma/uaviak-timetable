from typing import TYPE_CHECKING

from utils import DrawnTable, Cell, get_bytes_image
from vk_bot.core.timetable import WHOSE_TIMETABLE_TO_STRING, TYPES_TO_STRING

if TYPE_CHECKING:
    from db.structures import TimetableForSomeone, TypesLesson


class TimetablePhoto:
    BACKGROUND_TITLE_TABLE = (233, 233, 233)

    def __init__(self, timetable: 'TimetableForSomeone', font: str, size_font: int):
        self.timetable = timetable

        self.font = font
        self.size_font = size_font

    def _get_types_lesson_in_timetable(self) -> set['TypesLesson']:
        """Возвращает все типы пар в расписании.

        Returns:
            Типы пар в расписании.
        """
        types = set()
        for lesson in self.timetable.lessons:
            for type_ in lesson.types:
                types.add(type_)
        return types

    def _draw_title_table(self, drawn_table: DrawnTable) -> None:
        for i in ('№', 'Каб.', WHOSE_TIMETABLE_TO_STRING.get(self.timetable.whose_timetable), 'Предмет'):
            drawn_table.append(Cell(i, background_color=self.BACKGROUND_TITLE_TABLE))

    def _draw_lessons_information(self, drawn_table: DrawnTable) -> None:
        for lesson in self.timetable.lessons:
            drawn_table.row()
            drawn_table.append(Cell(str(lesson.number)))
            drawn_table.append(Cell(lesson.cabinet))
            drawn_table.append(Cell(lesson.whose))
            drawn_table.append(Cell(lesson.subject))

    def _draw_types_lesson(self, drawn_table: DrawnTable) -> None:
        timetable_types_lessons = self._get_types_lesson_in_timetable()
        for type_ in timetable_types_lessons:
            drawn_table.append(Cell(TYPES_TO_STRING.get(type_), background_color=self.BACKGROUND_TITLE_TABLE), row=0)
            for n_lesson, lesson in enumerate(self.timetable.lessons):
                n_row = n_lesson + 1

                if type_ in lesson.types:
                    text_cell = '+'
                else:
                    text_cell = '-'
                drawn_table.append(Cell(text_cell), row=n_row)

    def draw_photo_timetable(self) -> bytes:
        drawn_table = DrawnTable(self.font, self.size_font)

        self._draw_title_table(drawn_table)
        self._draw_lessons_information(drawn_table)
        self._draw_types_lesson(drawn_table)

        return get_bytes_image(drawn_table.draw())
