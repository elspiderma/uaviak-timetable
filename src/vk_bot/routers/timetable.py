from typing import TYPE_CHECKING

from vkbottle.bot import Blueprint

from vk_bot.search import search_lessons
from vk_bot.view import TimetableText, generate_keyboard_date

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
    results = await search_lessons(msg.text)

    if len(results) == 0:
        await msg.answer('Ничего не найдено.')
    elif len(results) == 1:
        result = results[0]

        dates = await result.get_dates_timetable()
        date = dates[0]

        timetable = await result.get_timetable(date)

        kb = generate_keyboard_date(dates, date, timetable)
        message = TimetableText(timetable).generate_text()

        await msg.answer(message, keyboard=kb.get_json(), reply_to=msg.id)
    else:
        await msg.answer('Найдено несколько результатов.')
