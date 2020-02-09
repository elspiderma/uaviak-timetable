import config

from vk_bot import VKBot
from vk_bot import VKBaseError

from timetable_text import TimetableText

from db import session, VKUser


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


def notify_enable(obj):
    local_session = session()
    user_db = local_session.query(VKUser).filter_by(id_vk=obj['message']['from_id']).first()
    if user_db is None:
        user_db = VKUser(id_vk=obj['message']['from_id'])
        local_session.add(user_db)

    group_name = obj['message']['text'][4:]
    timetable = TimetableText()
    find_groups = timetable.get_list_group(group_name)

    if len(find_groups) == 1:
        user_db.enable_notify = True
        user_db.group_notify = find_groups[0]
        text = f'Уведомления включены для группы \"{find_groups[0]}\"'
    elif len(find_groups) > 1:
        text = 'Найдено несколько групп, пожалуйста, выбирите одну.\n'
        text += f'Найденные группы: {", ".join(find_groups)}'
    else:
        text = 'Группа не найдена'

    local_session.commit()

    bot.messages_send(
        message=text,
        peer_id=obj['message']['peer_id'],
        reply_to=obj['message']['id']
    )


def notify_disable(obj):
    local_session = session()
    user_db = local_session.query(VKUser).filter_by(id_vk=obj['message']['from_id']).first()
    if user_db is None:
        user_db = VKUser(id_vk=obj['message']['from_id'])
        local_session.add(user_db)

    if user_db.enable_notify:
        user_db.enable_notify = False
        text = 'Уведомления выключены'
    else:
        text = 'Уведомления уже выключены\n\nДля включения напишите:\nувд номер_группы'

    local_session.commit()

    bot.messages_send(
        message=text,
        peer_id=obj['message']['peer_id'],
        reply_to=obj['message']['id']
    )


def send_notify(obj):
    if obj['message']['peer_id'] not in (70140946, 186973258):
        return send_timetable(obj)

    local_session = session()
    users = local_session.query(VKUser).filter_by(enable_notify=True).all()

    id_message = bot.messages_send(
        message="Рассылка...",
        peer_id=obj['message']['peer_id'],
        reply_to=obj['message']['id']
    )

    timetable = TimetableText()
    fail_user = 0
    for i in users:
        text = 'Выставлено новое расписание:\n\n'
        text += timetable.get_text_group(i.group_notify)
        try:
            bot.messages_send(
                message=text,
                peer_id=i.id_vk,
            )
        except VKBaseError:
            fail_user += 1

    bot.messages_edit(
        peer_id=obj['message']['peer_id'],
        message=f'Рассылка окончена!\nСообщений разослано: {len(users)}\nНеудачно: {fail_user}',
        message_id=id_message
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


bot = VKBot(config.TOKEN_BOT)
bot.message_new_handler_add(timetable_teacher, head_message="п ", ignore_case=True)
bot.message_new_handler_add(timetable_group, head_message="г ", ignore_case=True)
bot.message_new_handler_add(call_schedule, text_message=["з", "звонки"], ignore_case=True)
bot.message_new_handler_add(notify_disable, text_message='увд', ignore_case=True)
bot.message_new_handler_add(notify_enable, head_message="увд ", ignore_case=True)
bot.message_new_handler_add(send_notify, text_message="upd", ignore_case=True)
bot.message_new_handler_add(send_help, text_message="команды", ignore_case=True)
bot.message_new_handler_add(send_timetable)

if __name__ == '__main__':
    bot.polling(config.GROUP_ID, wait=10)
