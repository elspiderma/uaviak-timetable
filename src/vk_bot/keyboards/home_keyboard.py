from vkbottle import Keyboard, Text


def get_home_keyboard() -> Keyboard:
    return Keyboard() \
        .add(Text('Звонки')) \
        .add(Text('Настройки'))
