import config
from vk_bot.vk_bot import VKBot
import timetable_text
from random import randint
from uaviak_timetable import Timetable

from db import session, VKUser


def timetable_teacher(obj):
    teacher_name = obj['message']['text'][2:]

    text_timetable = timetable_text.teacher(teacher_name)
    if text_timetable is None:
        text_timetable = 'Преподователь не найден'

    bot.vk_api.messages.send(
        message=text_timetable,
        random_id=randint(0, 9999999),
        peer_id=obj['message']['peer_id'],
        reply_to=obj['message']['id']
    )


def timetable_group(obj):
    group_name = obj['message']['text'][2:]

    text_timetable = timetable_text.group(group_name)
    if text_timetable is None:
        text_timetable = 'Группа не найдена'

    bot.vk_api.messages.send(
        message=text_timetable,
        random_id=randint(0, 9999999),
        peer_id=obj['message']['peer_id'],
        reply_to=obj['message']['id']
    )


def call_schedule(obj):
    bot.vk_api.messages.send(
        message='Расписание звонков',
        attachment=config.PHOTO_CALLS,
        random_id=randint(0, 9999999),
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
    find_groups = timetable_text.is_exist_group(group_name)

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

    bot.vk_api.messages.send(
        message=text,
        random_id=randint(0, 9999999),
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

    bot.vk_api.messages.send(
        message=text,
        random_id=randint(0, 9999999),
        peer_id=obj['message']['peer_id'],
        reply_to=obj['message']['id']
    )


def send_notify(obj):
    if obj['message']['peer_id'] not in (70140946, 186973258):
        return not_found(obj)

    local_session = session()
    users = local_session.query(VKUser).filter_by(enable_notify=True).all()

    bot.vk_api.messages.send(
        message="Обновлено",
        random_id=randint(0, 9999999),
        peer_id=obj['message']['peer_id'],
        reply_to=obj['message']['id']
    )

    tt = Timetable.load()
    for i in users:
        text = 'Выставлено новое расписание:\n\n'
        text += timetable_text.group(i.group_notify, tt)
        try:
            bot.vk_api.messages.send(
                message=text,
                random_id=randint(0, 9999999),
                peer_id=i.id_vk,
            )
        except Exception:
            pass


def not_found(obj):
    text = \
        'Команда не найдена\n\n' \
        'Чтобы посмотреть расписание группы напишите:\n' \
        'г номер_группы\n\n' \
        'Чтобы посмотреть расписание преподавателя напишите:\n' \
        'п фамилия\n\n' \
        'Чтобы посмотреть расписание звонков напишите:\n' \
        '"з" или "звонки"\n\n' \
        'Если вы хотите получать уведомление при обновлении расписания напишите:\n' \
        'увд номер\n\n' \
        'Писать номер и фамилию можно не полностью, например, вместо "г 19ис-1" можно написать "г 19ис" или "г 19".\n' \
        'В номерах группы игнорируется тире, т.е. можно писать "г 19ис-1" можно писать "г 19ис1"'

    bot.vk_api.messages.send(
        message=text,
        random_id=randint(0, 9999999),
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
bot.message_new_handler_add(not_found)

if __name__ == '__main__':
    bot.polling(config.GROUP_ID)
