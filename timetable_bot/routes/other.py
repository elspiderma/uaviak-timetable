from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.bot import ChatActionRule
from vkbottle_types.objects import MessagesMessageActionStatus

bp = Blueprint(name="Other")
bp.labeler.vbml_ignore_case = True


@bp.on.message(text=['команды', 'помощь'])
async def send_help(msg: Message):
    """Помощь по боту."""
    text = """Список команд:
    \"увд номер_группы или имя_преподавателя\" - включить уведомления
    \"з\" или \"звонки\" - расписание звонков
    \"п фамилия\" - посмотреть расписание преподавателя
    \"г фамилия\" - посмотреть расписание группы

    Посмотреть расписание просто написав номер группы или фамилию преподавателя.
    Можно писать фамилию и номер неполностью, например, вместо \"19ис-1\" можно написать \"19ис\"."""

    await msg.answer(text, reply_to=msg.id)


@bp.on.chat_message(ChatActionRule([MessagesMessageActionStatus.CHAT_INVITE_USER]))
async def add_chat(msg: Message):
    """Новая беседа."""
    await msg.answer('Для включения уведомлений напишите:\n/увд <номер_группы_или_преподавателя>.\n\n'
              'Для отключения повторите команду.')
