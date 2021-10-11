import datetime
from typing import TYPE_CHECKING

from PIL import Image

from utils import DrawnTable, Cell
from vk_bot.keyboards import generate_keyboard_date
from vk_bot.search.result.abstract_result import AbstractResult
from vk_bot.timetable import WHOSE_TIMETABLE_TO_STRING, TYPES_TO_STRING

if TYPE_CHECKING:
    from db.structures import TimetableForSomeone, TypesLesson


class TimetablePhoto:
    BACKGROUND_TITLE_TABLE = (233, 233, 233)

    def __init__(self, timetable: 'TimetableForSomeone'):
        self.timetable = timetable

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

    def generate(self) -> Image:
        drawn_table = DrawnTable('NotoSans-Regular', 18)

        # Заголовки основных столбцов таблицы.
        for i in ('№', 'Каб.', WHOSE_TIMETABLE_TO_STRING.get(self.timetable.whose_timetable), 'Предмет'):
            drawn_table.append(Cell(i, background_color=self.BACKGROUND_TITLE_TABLE))

        # Заполнение основных столбцов таблицы.
        for lesson in self.timetable.lessons:
            drawn_table.row()
            drawn_table.append(Cell(str(lesson.number)))
            drawn_table.append(Cell(lesson.cabinet))
            drawn_table.append(Cell(lesson.whose))
            drawn_table.append(Cell(lesson.subject))

        # Поля с типами пар (опциональные стобцы).
        timetable_types_lessons = self._get_types_lesson_in_timetable()
        for type_ in timetable_types_lessons:
            drawn_table.append(Cell(TYPES_TO_STRING.get(type_), background_color=self.BACKGROUND_TITLE_TABLE))
            for n_lesson, lesson in enumerate(self.timetable.lessons):
                n_row = n_lesson + 1

                if type_ in lesson.types:
                    text_cell = '+'
                else:
                    text_cell = '-'
                drawn_table.append(Cell(text_cell), row=n_row)

        return drawn_table.draw()
