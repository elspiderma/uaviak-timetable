from typing import TYPE_CHECKING

from vkbottle.bot import Blueprint

from vk_bot.keyboards import generate_select_timetable_keyboard
from vk_bot.keyboards.payloads import TimetableDatePayload
from vk_bot.rules import PayloadRule
from vk_bot.search import search_by_query, search_by_payload
from vk_bot.view import get_message_timetable_for_result_search

if TYPE_CHECKING:
    from vkbottle.bot import Message

bp = Blueprint()
bp.labeler.vbml_ignore_case = True


@bp.on.private_message(PayloadRule(TimetableDatePayload))
async def search_timetable_for_date(msg: 'Message'):
    """Расписание для другого дня. Срабатывает при нажатии на кнопку с датой.

    Args:
        msg: Сообщение.
    """
    payload = TimetableDatePayload.from_dict(msg.get_payload_json())
    result = await search_by_payload(payload)

    message, keyboard_json = await get_message_timetable_for_result_search(result, payload.date)
    await msg.answer(message, keyboard=keyboard_json, reply_to=msg.id)


@bp.on.private_message()
async def search_timetable(msg: 'Message') -> None:
    """Поиск расписание по номеру группы/ФИО преподавателя.

    Args:
        msg: Сообщение
    """
    results = await search_by_query(msg.text)

    if len(results) == 0:
        await msg.answer('Распиание для преподавателя/группы не надено.', reply_to=msg.id)
    elif len(results) == 1:
        message, keyboard_json = await get_message_timetable_for_result_search(results[0])
        await msg.answer(message, keyboard=keyboard_json, reply_to=msg.id)
    else:
        kb = generate_select_timetable_keyboard(results)
        await msg.answer('Найдено несколько результатов.', keyboard=kb.get_json(), reply_to=msg.id)
