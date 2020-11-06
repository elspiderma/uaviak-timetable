import enum
from vkbottle.bot import Blueprint, Message

from timetable.timetable_text import TimetableText
import requests

bp = Blueprint(name="Query timetable")


class TypeTimetable(enum.Enum):
    TEACHER = enum.auto()
    GROUP = enum.auto()


async def get_timetable_text(type_: TypeTimetable, query: str, message_not_found: str):
    """Получение расписания для группы (`type_ == TypeTimetable.GROUP`) или
        преподавателя (`type_ == TypeTimetable.TEACHER`).
    Если расписание подходящее под `query` не найдено, то будет возвращено `message_not_found`.
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
    await msg(await get_timetable_text(TypeTimetable.TEACHER, name, 'Преподователь не найден'), reply_to=msg.id)


@bp.on.message(text=['г <number>', 'группа <number>'], lower=True)
async def timetable_group(msg: Message, number: str):
    await msg(await get_timetable_text(TypeTimetable.GROUP, number, 'Группа не найдена'), reply_to=msg.id)


@bp.on.message()
async def timetable_all(msg: Message):
    query = msg.text
    message_not_found = 'Группа или преподаватель не найден'

    if query[0].isnumeric():
        await msg(await get_timetable_text(TypeTimetable.GROUP, query, message_not_found), reply_to=msg.id)
    else:
        await msg(await get_timetable_text(TypeTimetable.TEACHER, query, message_not_found), reply_to=msg.id)
