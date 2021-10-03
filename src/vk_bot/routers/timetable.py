from typing import TYPE_CHECKING

from vkbottle.bot import Blueprint

from vk_bot.core import search_lessons

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
        timetable_group = await result.get_timetable(dates[0])

        await msg.answer(f'Подходящие даты: {dates}')
        await msg.answer(timetable_group)
    else:
        await msg.answer('Найдено несколько результатов.')

