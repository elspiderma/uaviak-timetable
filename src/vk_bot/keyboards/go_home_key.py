from vkbottle import Keyboard, Text, KeyboardButtonColor

from vk_bot.keyboards.payloads import GoHomePayload


def add_go_home_key(kb: Keyboard):
    kb.add(Text('На главную', payload=GoHomePayload().to_dict()), color=KeyboardButtonColor.PRIMARY)
