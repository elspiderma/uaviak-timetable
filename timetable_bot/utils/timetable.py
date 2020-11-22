from typing import TYPE_CHECKING

from tortoise.functions import Max

import db

if TYPE_CHECKING:
    from datetime import date


async def get_last_date_timetable() -> 'date':
    """ Получает дату последнего расписания. """
    last_date = await db.Timetable.annotate(last_date=Max('date')).values_list('last_date', flat=True)
    return last_date[0]


def is_group(s: str) -> bool:
    """Проверяет, является ли строка номером группы.

    @param s: Строка для проверки.
    @return: True - если номер группы, иначе False.
    """
    # Номера групп всегда начинаются на цифры.
    # Например 19ис-1, 18ом-1.
    return s[0].isnumeric()
