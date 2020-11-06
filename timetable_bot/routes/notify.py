from vkbottle import VKError
from vkbottle.bot import Blueprint, Message

from db import session, Notify
from main import bot
from timetable.timetable_text import TimetableText
from utils.random import get_random
from utils.rules import AdminMessage

bp = Blueprint(name="Notify")


@bp.on.chat_message(text='/увд <group_or_teacher>', lower=True)
@bp.on.message(text='увд <group_or_teacher>', lower=True)
async def notify_config(msg: Message, group_or_teacher: str):
    is_group: bool = group_or_teacher[0].isnumeric()

    timetable = await TimetableText.load()
    if is_group:
        objs_find = timetable.get_list_group(group_or_teacher)
    else:
        objs_find = timetable.get_list_teacher(group_or_teacher)

    if len(objs_find) > 1:
        text = f'Найдено несколько {"групп" if is_group else "преподователей"}: {", ".join(objs_find)}\n' \
               f'Повторите команду, написав {"полный номер группы" if is_group else "полное имя преподователя"}'
        await msg(text)
        return
    elif len(objs_find) == 0:
        await msg('Группа не найдена' if is_group else 'Преподователь не найден')
        return

    exist_notify = session.query(Notify).filter_by(
        id_vk=msg.peer_id,
        is_group=is_group,
        search_text=objs_find[0]
    ).first()

    if exist_notify is None:
        session.add(Notify(
            id_vk=msg.peer_id,
            is_group=is_group,
            search_text=objs_find[0]
        ))
        text = f'Уведомления для {"группы" if is_group else "преподователя"} "{objs_find[0]}" включены'
    else:
        session.delete(exist_notify)
        text = f'Уведомления для {"группы" if is_group else "преподователя"} "{exist_notify.search_text}" выключены'

    session.commit()

    await msg(text, reply_to=msg.id)


async def mailing_timetable(mailing_user: dict, initiator: int):
    """Рассылка уведомлений
    Словарь `mailing_user` должен иметь следующую структуру:
    ```
    {
        "ID_VK1": ["TIMETABLE1", "TIMETABLE2", "TIMETABLE3"],
        "ID_VK2": ["TIMETABLE4", "TIMETABLE5"],
    }
    ```
    """
    SEP = '\n\n'
    for vk_id, text_groups in mailing_user.items():
        if len(text_groups) == 0:
            continue

        text = f'Выставлено новое расписание:\n\n{SEP.join(text_groups)}'
        try:
            await bp.api.messages.send(peer_id=vk_id, message=text, random_id=get_random())
        except VKError as e:
            # Уведомление об ошибке отправки сообщения.
            text = f'Ошибка отправки сообщения.\n\nПользователь: {vk_id}\nТекст: {e.args}'
            await bp.api.messages.send(peer_id=70140946, message=text, random_id=get_random())
            if e.error_code in (7, 901):
                session.query(Notify).filter_by(id_vk=vk_id).delete()

    session.commit()

    await bp.api.messages.send(peer_id=initiator, message='Рассылка закончина', random_id=get_random())


@bp.on.message(AdminMessage(), text='upd', lower=True)
async def notify_send(msg: Message):
    timetable = await TimetableText.load()

    notify_users = session.query(Notify).all()

    texts = {}
    for user in notify_users:
        if user.id_vk not in texts:
            texts[user.id_vk] = list()

        if user.is_group:
            text = timetable.get_text_group(user.search_text)
        else:
            text = timetable.get_text_teacher(user.search_text)

        if text is not None:
            texts[user.id_vk].append(text)

    bot.loop.create_task(mailing_timetable(texts, msg.peer_id))