from vkbottle import Keyboard

from vk_bot.keyboards import add_go_home_key


def get_empty_keyboard() -> Keyboard:
    return add_go_home_key(Keyboard())
