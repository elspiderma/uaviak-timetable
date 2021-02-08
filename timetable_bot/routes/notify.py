from vkbottle.bot import Blueprint, Message

from core import TimetableTeacherModel, TimetableGroupModel, Chat
from utils.timetable import is_group

bp = Blueprint(name="Notify")
bp.labeler.vbml_ignore_case = True


@bp.on.chat_message(text='/увд <group_or_teacher>')
@bp.on.message(text='/увд <group_or_teacher>')
async def notify_config(msg: Message, group_or_teacher: str):
    """Включает (если включено, отключает), уведомление для группы или преподавателя."""
    chat = await Chat.get_by_id(msg.peer_id)
    if is_group(group_or_teacher):
        timetable = await TimetableGroupModel.for_last_day()
    else:
        timetable = await TimetableTeacherModel.for_last_day()

    objects_for_subscription = await timetable.search(group_or_teacher, True)

    if len(objects_for_subscription) == 1:
        obj = objects_for_subscription[0]
        if not await chat.is_subscribe_notify(obj):
            await chat.subscribe_notify(obj)
            await msg.answer(f'Уведомления для группы "{obj.name if hasattr(obj, "name") else obj.title}" включены')
        else:
            await chat.unsubscribe_notify(obj)
            await msg.answer(f'Уведомления для группы "{obj.name if hasattr(obj, "name") else obj.title}" выключены')
    elif len(objects_for_subscription) == 0:
        # TODO: Сообщение, о том, что объекты не найдены.
        pass
    else:
        # TODO: Сообщение о том, что найдено несколько объектов.
        pass
