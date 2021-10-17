from typing import TYPE_CHECKING

from vkbottle.bot import Blueprint
from vkbottle.dispatch.rules.bot import CommandRule

from vk_bot.core import get_photo_id_call_timetable
from vk_bot.keyboards import get_home_keyboard
from vk_bot.keyboards.payloads import GoHomePayload, CallTimetablePayload
from vk_bot.rules import PayloadRule

if TYPE_CHECKING:
    from vkbottle.bot import Message

bp = Blueprint()
bp.labeler.vbml_ignore_case = True


@bp.on.private_message(PayloadRule(GoHomePayload))
@bp.on.private_message(CommandRule('главная'))
async def send_home_keyboard(msg: 'Message') -> None:
    """Переходит на главное меню. Срабатывает по нажатию на кнопку "На главное меню" или по команде "/главная".

    Args:
        msg: Сообщение.
    """
    try:
        await bp.state_dispenser.delete(msg.peer_id)
    except KeyError:
        # Игнорирует отсутствие пользователя в state_dispenser
        pass

    kb = get_home_keyboard()
    await msg.answer('Главная', keyboard=kb.get_json(), reply_to=msg.id)


@bp.on.private_message(PayloadRule(CallTimetablePayload), state=None)
@bp.on.message(CommandRule('звонки'), state=None)
async def call_timetable(msg: 'Message') -> None:
    """Отправляет расписание звонков. Срабатывает по нажатию на кнопку "Звонки" или по команде "/звонки".

    Args:
        msg: Сообщение.
    """
    photo_id = await get_photo_id_call_timetable(bp.api)
    await msg.answer('Расписание звонков', attachment=photo_id, reply_to=msg.id)
