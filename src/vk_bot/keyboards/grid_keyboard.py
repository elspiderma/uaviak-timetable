from dataclasses import dataclass
from typing import TYPE_CHECKING

from vkbottle import Keyboard, KeyboardButtonColor

if TYPE_CHECKING:
    from vkbottle import ABCAction


@dataclass(frozen=True)
class Key:
    """Клавиша клавиатуры.

    Attributes:
        action: Действие кнопки.
        color: Цвет кнопки.
    """
    action: 'ABCAction'
    color: 'KeyboardButtonColor' = KeyboardButtonColor.SECONDARY


def generate_grid_keyboard(keys: list[Key], width: int, keyboard: Keyboard = None) -> Keyboard:
    """Формирует клавиатуру из клавиш keys с не более width клавиш в строке.

    Args:
        keys: Клавиши.
        width: Максимальное кол-во клавиш в строке.
        keyboard: Клавиатура, если None, то создает новую.

    Returns:
        Клавиатура из клавиш keys.
    """
    kb = keyboard if keyboard is not None else Keyboard()

    try:
        kb.row()
    except RuntimeError:
        # Игнорируем исключение, если ряд и так пустой.
        pass

    for n, i in enumerate(keys):
        if n != 0 and n % width == 0:
            kb.row()

        kb.add(i.action, i.color)

    return kb
