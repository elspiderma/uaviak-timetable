from db import Database

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from db.structures import ObjectWithTitleAndId


async def get_notify_message(chat_id: int) -> str:
    db = Database.from_keeper()

    result: list['ObjectWithTitleAndId'] = await db.get_user_subscriptions_group(chat_id)
    result += await db.get_user_subscriptions_teacher(chat_id)

    message_lines = [
        'Для добавления или удаления подписки напишите номер группы/ФИО преподавателя.',
        '',
        'Ваши подписки:'
    ]
    message_lines += [i.title for i in result]

    return '\n'.join(message_lines)
