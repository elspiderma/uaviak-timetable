from typing import TYPE_CHECKING

from vkbottle import Keyboard, Text

from db.structures import WhoseTimetable
from vk_bot.keyboards import Key, generate_grid_keyboard, add_go_home_key
from vk_bot.keyboards.payloads import ResultPayload

if TYPE_CHECKING:
    from vk_bot.search import AbstractResult


class TooMuchResultInKeyboardError(Exception):
    pass


def generate_select_timetable_keyboard(results: list['AbstractResult']) -> Keyboard:
    """Клавиатура из результатов поиска results.

    Args:
        results: Список результатов поиска.

    Returns:
        Клавиатура из результатов поиска results.

    Raises:
        TooMuchResultInKeyboardError: Передано слишком много результатов поиска.
    """
    count_in_row = 3
    # Т.к. ФИО проподавателей длинее, чем номера групп, то формируем их в 2 стобца
    if WhoseTimetable.FOR_TEACHER in [i.whose for i in results]:  # Вообще, такой способ проверки -- костыль, но кого это волнует...
        count_in_row = 2

    limit_result = 9 * count_in_row
    if len(results) > limit_result:
        raise TooMuchResultInKeyboardError(f'Too much keys in keyboard (Max {limit_result}).')

    kb = Keyboard(inline=False, one_time=False)
    generate_grid_keyboard(
        [Key(Text(i.title, payload=ResultPayload(i.id, i.whose).to_dict())) for i in results],
        count_in_row,
        kb
    )

    kb.row()
    add_go_home_key(kb)
    return kb
