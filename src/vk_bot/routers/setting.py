from typing import TYPE_CHECKING

from vkbottle.bot import Blueprint

from db import Database
from vk_bot import StateDispenser
from vk_bot.core import get_notify_message
from vk_bot.keyboards import get_setting_keyboard, get_notify_keyboard
from vk_bot.keyboards.payloads import SettingMenuPayload, ChangeFormatTimetablePayload, NotifySettingPayload
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
    await msg.answer(await get_notify_message(msg.peer_id), keyboard=get_notify_keyboard().get_json())
    await bp.state_dispenser.set(msg.peer_id, StateDispenser.NOTIFY_SETTING)


@bp.on.private_message(state=StateDispenser.NOTIFY_SETTING)
async def notify_object(msg: 'Message'):
    """Включает/выключает уведомления. Срабатывает при отправки сообщения в режиме настройки уведомлений.

    Args:
        msg: Сообщение.
    """
    await msg.answer(await get_notify_message(msg.peer_id))
