from typing import TYPE_CHECKING

from vkbottle.bot import Blueprint

if TYPE_CHECKING:
    from vkbottle.bot import Message

bp = Blueprint()
bp.labeler.vbml_ignore_case = True


@bp.on.private_message(text=['Проверка'])
async def test_message(msg: 'Message'):
    await msg.answer('привет', reply_to=msg.id)
