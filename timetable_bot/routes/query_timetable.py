import enum

import requests
from vkbottle.bot import Blueprint, Message

from timetable.timetable_text import TimetableText

bp = Blueprint(name="Query timetable")


class TypeTimetable(enum.Enum):
    TEACHER = enum.auto()
    GROUP = enum.auto()


async def get_timetable_text(type_: TypeTimetable, query: str, message_not_found: str):
    """Получение расписания для группы/преподавателя.

    @param type_: Тип поиска. `TypeTimetable.TEACHER` поиск по преподавателям. `TypeTimetable.GROUP` поиск по группе.
    @param query: Шаблон поиска.
    @param message_not_found: Сообзение, которое будет возвращено, если не найдено `query`.
    @return:
    """
    try:
        timetable = await TimetableText.load()
    except requests.exceptions.ConnectionError:
        return 'Не могу получить расписание :('

    if type_ == TypeTimetable.GROUP:
        text = timetable.get_text_group(query)
    elif type_ == TypeTimetable.TEACHER:
        text = timetable.get_text_teacher(query)
    else:
        raise ValueError()

    if text is None:
        return message_not_found

    return text


@bp.on.message(text=['п <name>', 'группа <number>'], lower=True)
async def timetable_teacher(msg: Message, name: str):
    """Расписание преподавателя."""
    await msg(await get_timetable_text(TypeTimetable.TEACHER, name, 'Преподователь не найден'), reply_to=msg.id)


@bp.on.message(text=['г <number>', 'группа <number>'], lower=True)
async def timetable_group(msg: Message, number: str):
    """Расписание группы."""
    await msg(await get_timetable_text(TypeTimetable.GROUP, number, 'Группа не найдена'), reply_to=msg.id)


@bp.on.message()
async def timetable_all(msg: Message):
    """Расписание группы/преподавателя."""
    query = msg.text
    message_not_found = 'Группа или преподаватель не найден'

    if query[0].isnumeric():
        await msg(await get_timetable_text(TypeTimetable.GROUP, query, message_not_found), reply_to=msg.id)
    else:
        await msg(await get_timetable_text(TypeTimetable.TEACHER, query, message_not_found), reply_to=msg.id)
