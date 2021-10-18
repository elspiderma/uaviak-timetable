from typing import TYPE_CHECKING

from vkbottle.bot import Blueprint

from db import Database
from vk_bot import StateDispenser
from vk_bot.core import get_notify_message, get_subscribes
from vk_bot.core.search import search_by_query, search_by_id
from vk_bot.keyboards import get_setting_keyboard, get_main_notify_keyboard, TooMuchResultInKeyboardError, \
    get_results_keyboard
from vk_bot.keyboards.payloads import SettingMenuPayload, ChangeFormatTimetablePayload, NotifySettingPayload, \
    ResultPayload, SubscribePayload, SubscribeAction
from vk_bot.rules import PayloadRule

if TYPE_CHECKING:
    from vkbottle.bot import Message

bp = Blueprint()
bp.labeler.vbml_ignore_case = True


@bp.on.private_message(PayloadRule(SettingMenuPayload), state=None)
async def setting(msg: 'Message') -> None:
    """Настройки бота. Срабатывает при нажатии на кнопку "Настройки" в главном меню.

    Args:
        msg: Сообщение.
    """
    db = Database.from_keeper()
    chat = await db.get_chat_and_create_if_not_exist(msg.peer_id)

    keyboard = get_setting_keyboard(chat)
    await msg.answer('Настройки', keyboard=keyboard.get_json())


@bp.on.private_message(PayloadRule(ChangeFormatTimetablePayload), state=None)
async def change_format_timetable(msg: 'Message'):
    """Переключает формат присылаемого расписания. Срабатывает при выборе в меню настроек "Формат расписания".

    Args:
        msg: Сообщение.
    """
    db = Database.from_keeper()
    chat = await db.get_chat_and_create_if_not_exist(msg.peer_id)

    await db.change_format_timetable_for_chat(chat)
    chat = await db.get_chat_and_create_if_not_exist(msg.peer_id)

    keyboard = get_setting_keyboard(chat)
    await msg.answer('Формат расписания изменен', keyboard=keyboard.get_json())


@bp.on.private_message(PayloadRule(NotifySettingPayload), state=None)
async def notify_setting(msg: 'Message') -> None:
    """Переходит в режим настройки уведомлений. Срабатывает при нажатии в меню настроек на кнопку "Уведомления".

    Args:
        msg: Сообщение.
    """
    subscribes = await get_subscribes(msg.peer_id)

    message_text = get_notify_message(subscribes)
    kb = get_main_notify_keyboard(subscribes)

    await msg.answer(message_text, keyboard=kb.get_json())
    await bp.state_dispenser.set(msg.peer_id, StateDispenser.NOTIFY_SETTING)


@bp.on.private_message(PayloadRule(SubscribePayload), state=StateDispenser.NOTIFY_SETTING)
async def subscribe_action(msg: 'Message'):
    db = Database.from_keeper()
    chat = await db.get_chat_and_create_if_not_exist(msg.peer_id)

    payload = SubscribePayload.from_dict(msg.get_payload_json())

    result = await search_by_id(payload.whose, payload.id)
    if payload.action == SubscribeAction.SUBSCRIBE:
        message = f'Добавлена подписка для {result.title}'
        await result.subscribe_user(chat)
    else:
        message = f'Удалена подписка для {result.title}'
        await result.unsubscribe_user(chat)

    subscribes = await get_subscribes(msg.peer_id)
    kb = get_main_notify_keyboard(subscribes)

    await msg.answer(message, keyboard=kb.get_json())


@bp.on.private_message(PayloadRule(ResultPayload), state=StateDispenser.NOTIFY_SETTING)
async def result_notify(msg: 'Message'):
    pass


@bp.on.private_message(state=StateDispenser.NOTIFY_SETTING)
async def notify_object(msg: 'Message'):
    """Включает/выключает уведомления. Срабатывает при отправки сообщения в режиме настройки уведомлений.

    Args:
        msg: Сообщение.
    """
    results = await search_by_query(msg.text)

    if len(results) == 0:
        await msg.answer('Преподаватель/группа не наден(а).', reply_to=msg.id)
    elif len(results) == 1:
        await msg.answer('Ok', reply_to=msg.id)
    else:
        try:
            kb = get_results_keyboard(results)
        except TooMuchResultInKeyboardError:
            await msg.answer('Слишком много результатов. Напишите запрос точнее.')
        else:
            await msg.answer('Найдено несколько результатов.', keyboard=kb.get_json(), reply_to=msg.id)
