import config

from vk_bot import VKBot
from vk_bot import VKBaseError

from timetable_text import TimetableText

from db import session, Notify


def send_timetable(obj):
    search_text = obj['message']['text']

    timetable = TimetableText()
    if search_text[0].isnumeric():
        text = timetable.get_text_group(search_text)
    else:
        text = timetable.get_text_teacher(search_text)

    if text is None:
        text = 'Группа или преподаватель не найден'

    bot.messages_send(
        message=text,
        peer_id=obj['message']['peer_id'],
        reply_to=obj['message']['id']
    )


def timetable_teacher(obj):
    teacher_name = obj['message']['text'][2:]

    timetable = TimetableText()
    text = timetable.get_text_teacher(teacher_name)
    if text is None:
        text = 'Преподователь не найден'

    bot.messages_send(
        message=text,
        peer_id=obj['message']['peer_id'],
        reply_to=obj['message']['id']
    )


def timetable_group(obj):
    group_name = obj['message']['text'][2:]

    timetable = TimetableText()
    text = timetable.get_text_group(group_name)
    if text is None:
        text = 'Группа не найдена'

    bot.messages_send(
        message=text,
        peer_id=obj['message']['peer_id'],
        reply_to=obj['message']['id']
    )


def call_schedule(obj):
    bot.messages_send(
        message='Расписание звонков',
        attachment=config.PHOTO_CALLS,
        peer_id=obj['message']['peer_id'],
        reply_to=obj['message']['id']
    )


def send_help(obj):
    text = """Список команд:
    \"увд номер_группы\" - включить уведомления
    \"увд\" - выключить уведомления
    \"з\" или \"звонки\" - расписание звонков
    \"п фамилия\" - посмотреть расписание преподавателя
    \"г фамилия\" - посмотреть расписание группы
    
    Посмотреть расписание просто написав номер группы или фамилию преподавателя.
    Можно писать фамилию и номер неполностью, например, вместо \"19ис-1\" можно написать \"19ис\"."""

    bot.messages_send(
        message=text,
        peer_id=obj['message']['peer_id'],
        reply_to=obj['message']['id']
    )


def notify(obj):
    local_session = session()

    head_obj = obj['message']['text'][4:]
    is_group = head_obj[0].isnumeric()

    exist_notify = local_session.query(Notify).filter_by(
        id_vk=obj['message']['peer_id'],
        is_group=is_group,
        search_text=head_obj
    ).first()

    if exist_notify is None:
        timetable = TimetableText()

        if is_group:
            objs_find = timetable.get_list_group(head_obj)
        else:
            objs_find = timetable.get_list_teacher(head_obj)

        if len(objs_find) == 1:
            local_session.add(Notify(
                id_vk=obj['message']['peer_id'],
                is_group=is_group,
                search_text=objs_find[0]
            ))
            text = f'Уведомления для {"группы" if is_group else "преподователя"} "{objs_find[0]}" включены'
        elif len(objs_find) > 1:
            text = f'Найдено несколько {"групп" if is_group else "преподователей"}: {", ".join(objs_find)}\n' \
                   f'Повторите команду, написав {"полный номер группы" if is_group else "полное имя преподователя"}'
        else:
            text = "Группа не найдена" if is_group else "Преподователь не найден"
    else:
        local_session.delete(exist_notify)
        text = f'Уведомления для {"группы" if is_group else "преподователя"} "{exist_notify.search_text}" выключены'

    local_session.commit()

    bot.messages_send(
        message=text,
        peer_id=obj['message']['peer_id'],
        reply_to=obj['message']['id']
    )


def notify_send(obj):
    if obj['message']['peer_id'] not in (70140946, 186973258):
        return send_timetable(obj)

    timetable = TimetableText()

    local_session = session()
    notify_users = local_session.query(Notify).all()

    texts = {}
    for i in notify_users:
        if i.id_vk not in texts:
            texts[i.id_vk] = list()

        if i.is_group:
            text = timetable.get_text_group(i.search_text)
        else:
            text = timetable.get_text_teacher(i.search_text)

        texts[i.id_vk].append(text)

    SEP = '\n\n'
    for vk_id, text_groups in texts.items():
        text = f'Выставлено новое расписание:\n\n{SEP.join(text_groups)}'
        bot.messages_send(
            message=text,
            peer_id=vk_id,
        )


bot = VKBot(config.TOKEN_BOT)
bot.message_new_handler_add(timetable_teacher, head_message='п ', ignore_case=True)
bot.message_new_handler_add(timetable_group, head_message='г ', ignore_case=True)
bot.message_new_handler_add(call_schedule, text_message=['з', 'звонки'], ignore_case=True)
bot.message_new_handler_add(notify, head_message='увд ', ignore_case=True)
bot.message_new_handler_add(notify_send, text_message='upd', ignore_case=True)
bot.message_new_handler_add(send_help, text_message='команды', ignore_case=True)
bot.message_new_handler_add(send_timetable)

if __name__ == '__main__':
    bot.polling(config.GROUP_ID, wait=10)
