import datetime
from typing import TYPE_CHECKING

from vkbottle import Keyboard, Text, KeyboardButtonColor

from vk_bot.keyboards import Key, generate_grid_keyboard, add_go_home_key
from vk_bot.keyboards.payloads import TimetableDatePayload

if TYPE_CHECKING:
    from vk_bot.core.search import AbstractResult


def generate_keyboard_date(dates: list[datetime.date], current_date: datetime.date, result: 'AbstractResult') \
        -> Keyboard:
    """Формирует клавиатуру из дат dates.

    Args:
        dates: Список дат.
        current_date: Текущая выбранная дата.
        timetable: Расписание.

    Returns:
        Клавиатура из дат dates.
    """

    keys = list()
    for i in dates:

        payload = TimetableDatePayload(
            date=i,
            id_=result.id,
            whose_timetable=result.whose
        )

        keys.append(
            Key(
                Text(i.strftime('%a %d.%m'), payload=payload.to_dict()),
                KeyboardButtonColor.POSITIVE if i == current_date else KeyboardButtonColor.SECONDARY
            )
        )

    kb = Keyboard(inline=False, one_time=False)
    generate_grid_keyboard(keys, 3, kb)

    kb.row()
    add_go_home_key(kb)
    return kb
