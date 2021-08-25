from typing import TYPE_CHECKING

from vkbottle import Keyboard
from vkbottle.bot import Blueprint

from db import ConnectionKeeper, Database

if TYPE_CHECKING:
    from vkbottle.bot import Message

bp = Blueprint()
bp.labeler.vbml_ignore_case = True


@bp.on.private_message()
async def search_timetable(msg: 'Message') -> None:
    """Поиск расписание по номеру группы/ФИО преподавателя (#TODO)

    Args:
        msg: Сообщение
    """
    db = Database(ConnectionKeeper.get_connection())

    groups = await db.search_group(msg.text)

    await msg.answer(f"Найденные группы: {', '.join([i.number for i in groups])}", reply_to=msg.id)
