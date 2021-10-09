from typing import TYPE_CHECKING

from vkbottle import Keyboard, Text
from vk_bot.keyboards import Key, generate_grid_keyboard

if TYPE_CHECKING:
    from vk_bot.search import AbstractResult


def generate_select_timetable_keyboard(results: list['AbstractResult']) -> Keyboard:
    """Клавиатура из результатов поиска results.

    Args:
        results: Список результатов поиска.

    Returns:
        Клавиатура из результатов поиска results.
    """
    kb = Keyboard(inline=False, one_time=False)
    generate_grid_keyboard([Key(Text(i.title)) for i in results], 3, kb)
    return kb
