import enum

from vkbottle.bot import Blueprint, Message

from models import TimetableModel
from view import TimetableTeacherView, TimetableGroupView


bp = Blueprint()
bp.labeler.vbml_ignore_case = True


class TypeTimetable(enum.Enum):
    TEACHER = enum.auto()
    GROUP = enum.auto()


async def get_timetable(type_: TypeTimetable, query: str, message_not_found: str):
    """Получает расписания для группы/преподавателя.

    @param type_: Тип поиска. `TypeTimetable.TEACHER` поиск по преподавателям. `TypeTimetable.GROUP` поиск по группе.
    @param query: Шаблон поиска.
    @param message_not_found: Сообщение, которое будет возвращено, если не найдено `query`.
    @return: Расписание, либо `message_not_found`.
    """

    timetable_db = await TimetableModel.for_last_day()
    MODEL_VIEW_LIST = {
        TypeTimetable.GROUP: {
            'model_list': timetable_db.get_groups,
            'model_timetable': timetable_db.get_timetable_for_group,
            'view': TimetableGroupView
        },
        TypeTimetable.TEACHER: {
            'model_list': timetable_db.get_teachers,
            'model_timetable': timetable_db.get_timetable_for_teacher,
            'view': TimetableTeacherView
        }
    }

    list_items_query = await MODEL_VIEW_LIST[type_]['model_list'](query, True)
    if len(list_items_query) == 0:
        return message_not_found

    list_timetables = [await MODEL_VIEW_LIST[type_]['model_timetable'](i) for i in list_items_query]
    text = MODEL_VIEW_LIST[type_]['view'].get_text(list_timetables)

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
