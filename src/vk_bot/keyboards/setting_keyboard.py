from typing import TYPE_CHECKING

from vkbottle import Keyboard, Text

from vk_bot.keyboards import add_go_home_key
from vk_bot.keyboards.payloads import ChangeFormatTimetablePayload, NotifySettingPayload

if TYPE_CHECKING:
    from db.structures import Chat


def get_setting_keyboard(chat: 'Chat') -> Keyboard:
    kb = Keyboard()

    format_timetable = 'фото' if chat.timetable_photo else 'текст'

    kb \
        .add(Text('Настройки уведомлений', payload=NotifySettingPayload().to_dict())) \
        .row() \
        .add(Text(f'Формат расписания: {format_timetable}', payload=ChangeFormatTimetablePayload().to_dict()))

    kb.row()
    add_go_home_key(kb)

    return kb
