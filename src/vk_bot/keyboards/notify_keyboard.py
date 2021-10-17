from vkbottle import Keyboard, KeyboardButtonColor, Text

from vk_bot.keyboards import add_go_home_key


def get_notify_keyboard() -> Keyboard:
    kb = Keyboard()

    kb.add(Text('Отключить все'), color=KeyboardButtonColor.NEGATIVE)

    kb.row()
    add_go_home_key(kb)

    return kb
