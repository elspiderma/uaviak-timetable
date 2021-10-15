from vkbottle import Keyboard, Text

from vk_bot.keyboards.payloads import CallTimetablePayload


def get_home_keyboard() -> Keyboard:
    return Keyboard() \
        .add(Text('Звонки', payload=CallTimetablePayload().to_dict())) \
        .add(Text('Настройки'))
