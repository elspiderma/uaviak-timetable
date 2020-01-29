import config
from vk_bot.vk_bot import VKBot
import timetable_text
from random import randint
from uaviak_timetable import Timetable

from db import session, VKUser


def timetable_teacher(obj):
    message_text = obj['message']['text']
    message_id = obj['message']['id']
    peer_id = obj['message']['peer_id']
    random_id = randint(0, 9999999)

    teacher_name = message_text[2:]

    text_timetable = timetable_text.teacher(teacher_name)
    if text_timetable is None:
        text_timetable = 'Преподователь не найден'

    bot.vk_api.messages.send(
        message=text_timetable,
        random_id=random_id,
        peer_id=peer_id,
        reply_to=message_id
    )


def timetable_group(obj):
    message_text = obj['message']['text']
    message_id = obj['message']['id']
    peer_id = obj['message']['peer_id']
    random_id = randint(0, 9999999)

    group_name = message_text[2:]

    text_timetable = timetable_text.group(group_name)
    if text_timetable is None:
        text_timetable = 'Группа не найдена'

    bot.vk_api.messages.send(
        message=text_timetable,
        random_id=random_id,
        peer_id=peer_id,
        reply_to=message_id
    )


def not_found(obj):
    message_id = obj['message']['id']
    peer_id = obj['message']['peer_id']
    random_id = randint(0, 9999999)

    text = \
        'Команда не найдена\n' \
        'Для того чтобы получить расписание группы напишите:\n' \
        'г номер_группы\n\n' \
        'Для того чтобы получить расписание преподователя напишите:\n' \
        'п фамилия\n\n' \
        'Писать номер и фамилию можно не полностью, например, вместо "г 19ис-1" можно написать "г 19ис" или "г 19"'

    bot.vk_api.messages.send(
        message=text,
        random_id=random_id,
        peer_id=peer_id,
        reply_to=message_id
    )


def notify(obj):
    message_text = obj['message']['text']
    message_id = obj['message']['id']
    peer_id = obj['message']['peer_id']
    user_id = obj['message']['from_id']
    random_id = randint(0, 9999999)

    user_db = session.query(VKUser).filter_by(id_vk=user_id).first()
    if user_db is None:
        user_db = VKUser(id_vk=user_id)
        session.add(user_db)
        session.commit()

    if user_db.enable_notify:
        user_db.enable_notify = False
        text = 'Уведомления выключены'
    else:
        group_name = message_text[4:]
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

    session.commit()

    bot.vk_api.messages.send(
        message=text,
        random_id=random_id,
        peer_id=peer_id,
        reply_to=message_id
    )


def send_notify(obj):
    if obj['message']['peer_id'] not in (70140946, 186973258):
        return not_found(obj)

    users = session.query(VKUser).filter_by(enable_notify=True).all()

    tt = Timetable.load()
    for i in users:
        text = timetable_text.group(i.group_notify, tt)
        try:
            bot.vk_api.messages.send(
                message=text,
                random_id=randint(0, 9999999),
                peer_id=i.id_vk,
            )
        except Exception:
            pass


bot = VKBot(config.TOKEN_BOT)
bot.message_new_handler_add(timetable_teacher, head_message="п ", ignore_case=True)
bot.message_new_handler_add(timetable_group, head_message="г ", ignore_case=True)
bot.message_new_handler_add(notify, head_message="увд", ignore_case=True)
bot.message_new_handler_add(send_notify, head_message="upd", ignore_case=True)
bot.message_new_handler_add(not_found)

if __name__ == '__main__':
    bot.polling(config.GROUP_ID)
