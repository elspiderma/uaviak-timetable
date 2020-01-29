import config
from vk_bot.vk_bot import VKBot
import timetable_text
from random import randint


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


bot = VKBot(config.TOKEN_BOT)
bot.message_new_handler_add(timetable_teacher, head_message="п ", ignore_case=True)
bot.message_new_handler_add(timetable_group, head_message="г ", ignore_case=True)
bot.message_new_handler_add(not_found)

if __name__ == '__main__':
    bot.polling(config.GROUP_ID)
