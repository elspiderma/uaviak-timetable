import datetime
import enum
from typing import TYPE_CHECKING

from vkbottle import Keyboard, Text, KeyboardButtonColor

from db.structures import TimetableForGroup, TimetableForTeacher

if TYPE_CHECKING:
    from db.structures import TimetableForSomeone


class TypeKeyboardDate(enum.Enum):
    FOR_TEACHER = enum.auto()
    FOR_GROUP = enum.auto()


def _generate_keyboard_date(dates: list[datetime.date], current_date: datetime.date, type_: TypeKeyboardDate, id_) \
        -> Keyboard:
    kb = Keyboard(inline=False, one_time=False)

    for n, i in enumerate(dates):
        if n != 0 and n % 2 == 0:
            kb.row()

        kb.add(Text(i.strftime('%a %d.%m'), payload={'a': 1}),
               color=KeyboardButtonColor.POSITIVE if i == current_date else KeyboardButtonColor.SECONDARY)

    return kb


def generate_keyboard_date(dates: list[datetime.date], current_date: datetime.date, timetable: 'TimetableForSomeone') \
        -> Keyboard:
    if isinstance(timetable, TimetableForGroup):
        return _generate_keyboard_date(dates, current_date, TypeKeyboardDate.FOR_GROUP, timetable.group.id)
    elif isinstance(timetable, TimetableForTeacher):
        return _generate_keyboard_date(dates, current_date, TypeKeyboardDate.FOR_TEACHER, timetable.teacher.id)
    else:
        raise ValueError()
