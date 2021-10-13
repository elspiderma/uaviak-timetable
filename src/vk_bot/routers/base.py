from typing import TYPE_CHECKING

from vkbottle.bot import Blueprint

from vk_bot.keyboards import get_home_keyboard
from vk_bot.keyboards.payloads import GoHomePayload
from vk_bot.rules import PayloadRule

if TYPE_CHECKING:
    from vkbottle.bot import Message

bp = Blueprint()
bp.labeler.vbml_ignore_case = True


@bp.on.private_message(PayloadRule(GoHomePayload))
async def send_home_keyboard(msg: 'Message') -> None:
    kb = get_home_keyboard()
    await msg.answer('Главная', keyboard=kb.get_json())
