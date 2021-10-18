from vkbottle import Keyboard, KeyboardButtonColor, Text
from typing import TYPE_CHECKING

from vk_bot.keyboards import add_go_home_key
from vk_bot.keyboards.payloads import SubscribePayload, SubscribeAction

if TYPE_CHECKING:
    from vk_bot.core.search import AbstractResult


def get_main_notify_keyboard(subscribers: list['AbstractResult']) -> Keyboard:
    kb = Keyboard()

    for i in subscribers[:9]:
        button_action = Text(f'Отписатся от {i.title}',
                             payload=SubscribePayload(i.id, i.whose, SubscribeAction.UNSUBSCRIBE).to_dict())

        kb.add(button_action, color=KeyboardButtonColor.NEGATIVE)
        kb.row()

    add_go_home_key(kb)

    return kb
