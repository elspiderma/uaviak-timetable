from vkbottle.bot import Blueprint, Message

from utils.random import get_random

bp = Blueprint(name="Other")


@bp.on.message(text=['команды', 'помощь'], lower=True)
async def send_help(msg: Message):
    text = """Список команд:
    \"увд номер_группы или имя_преподавателя\" - включить уведомления
    \"з\" или \"звонки\" - расписание звонков
    \"п фамилия\" - посмотреть расписание преподавателя
    \"г фамилия\" - посмотреть расписание группы

    Посмотреть расписание просто написав номер группы или фамилию преподавателя.
    Можно писать фамилию и номер неполностью, например, вместо \"19ис-1\" можно написать \"19ис\"."""

    await msg(text, reply_to=msg.id)


@bp.on.chat_action('chat_invite_user')
async def add_chat(msg: Message):
    await msg.api.messages.send(peer_id=70140946, message=f'Новая беседа: {msg.peer_id}', random_id=get_random())
    await msg('Для включения уведомлений напишите:\n/увд <номер_группы_или_преподавателя>.\n\n'
              'Для отключения повторите команду.')
