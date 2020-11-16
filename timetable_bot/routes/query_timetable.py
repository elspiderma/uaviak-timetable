import enum

from vkbottle.bot import Blueprint, Message

from models import TimetableGroupModel, TimetableTeacherModel
from view import TimetableTeacherView, TimetableGroupView


bp = Blueprint()
bp.labeler.vbml_ignore_case = True


class TypeTimetable(enum.Enum):
    TEACHER = enum.auto()
    GROUP = enum.auto()

MODEL_VIEW_LIST = {
    TypeTimetable.GROUP: {
        'model': TimetableGroupModel,
        'view': TimetableGroupView
    },
    TypeTimetable.TEACHER: {
        'model': TimetableTeacherModel,
        'view': TimetableTeacherView
    }
}


async def get_timetable(type_: TypeTimetable, query: str, message_not_found: str):
    """Получает расписания для группы/преподавателя.

    @param type_: Тип поиска. `TypeTimetable.TEACHER` поиск по преподавателям. `TypeTimetable.GROUP` поиск по группе.
    @param query: Шаблон поиска.
    @param message_not_found: Сообщение, которое будет возвращено, если не найдено `query`.
    @return: Расписание, либо `message_not_found`.
    """
    Model = MODEL_VIEW_LIST[type_]['model']
    View = MODEL_VIEW_LIST[type_]['view']

    timetable_db = await Model.for_last_day()

    list_items_query = await timetable_db.search(query, True)
    if len(list_items_query) == 0:
        return message_not_found

    list_timetables = [await timetable_db.get_timetable(i) for i in list_items_query]
    text = View.get_text(list_timetables)

    return text


@bp.on.private_message(text=['п <name>', 'преподаватель <name>'])
async def timetable_teacher(msg: Message, name: str):
    """Расписание преподавателя."""
    await msg.answer(await get_timetable(TypeTimetable.GROUP, name, "Преподователь не найден"))


@bp.on.private_message(text=['г <title>', 'группа <title>'])
async def timetable_group(msg: Message, title: str):
    """Расписание группы."""
    await msg.answer(await get_timetable(TypeTimetable.GROUP, title, "Группа не найдена"))


@bp.on.private_message()
async def timetable_all(msg: Message):
    """Расписание группы/преподавателя."""
    query = msg.text

    # Номера групп всегда начинаются на цифры.
    # Например 19ис-1, 18ом-1.
    type_ = TypeTimetable.GROUP if query[0].isnumeric() else TypeTimetable.TEACHER
    await msg.answer(await get_timetable(type_, query, 'Группа или преподаватель не найден'))
