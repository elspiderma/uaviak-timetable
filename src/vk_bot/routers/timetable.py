from typing import TYPE_CHECKING

from vkbottle.bot import Blueprint

from vk_bot.keyboards import generate_select_timetable_keyboard, TooMuchResultInKeyboardError
from vk_bot.keyboards.payloads import TimetableDatePayload, ResultPayload
from vk_bot.rules import PayloadRule
from vk_bot.core.search import search_by_query, search_by_id
from vk_bot.core.timetable import get_message_timetable_for_result_search

if TYPE_CHECKING:
    from vkbottle.bot import Message

bp = Blueprint()
bp.labeler.vbml_ignore_case = True


@bp.on.private_message(PayloadRule(TimetableDatePayload))
async def search_timetable_for_date(msg: 'Message') -> None:
    """Расписание для другого дня. Срабатывает при нажатии на кнопку с датой.

    Args:
        msg: Сообщение.
    """
    payload = TimetableDatePayload.from_dict(msg.get_payload_json())
    result = await search_by_id(payload.whose_timetable, payload.id)

    message, photo_id, keyboard_json = await get_message_timetable_for_result_search(
        bp.api, msg.peer_id, result, payload.date
    )
    await msg.answer(message, keyboard=keyboard_json, reply_to=msg.id, attachment=photo_id)


@bp.on.private_message(PayloadRule(ResultPayload))
async def result_timetable(msg: 'Message') -> None:
    """Расписание для результата поиска. Срабатывает при нажатии на кнопку с выбором результата
        поиска преподавателя/группы.

    Args:
        msg: Сообщение
    """
    payload = ResultPayload.from_dict(msg.get_payload_json())
    result = await search_by_id(payload.whose_timetable, payload.id)

    message, photo_id, keyboard_json = await get_message_timetable_for_result_search(
        bp.api, msg.peer_id, result
    )
    await msg.answer(message, keyboard=keyboard_json, reply_to=msg.id, attachment=photo_id)


@bp.on.private_message()
async def search_timetable(msg: 'Message') -> None:
    """Поиск расписание по номеру группы/ФИО преподавателя.

    Args:
        msg: Сообщение
    """

    results = await search_by_query(msg.text)

    if len(results) == 0:
        await msg.answer('Расписание для преподавателя/группы не надено.', reply_to=msg.id)
    elif len(results) == 1:
        message, photo_id, keyboard_json = await get_message_timetable_for_result_search(
            bp.api, msg.peer_id, results[0]
        )
        await msg.answer(message, keyboard=keyboard_json, reply_to=msg.id, attachment=photo_id)
    else:
        try:
            kb = generate_select_timetable_keyboard(results)
        except TooMuchResultInKeyboardError:
            await msg.answer('Слишком много результатов. Напишите запрос точнее.')
        else:
            await msg.answer('Найдено несколько результатов.', keyboard=kb.get_json(), reply_to=msg.id)
