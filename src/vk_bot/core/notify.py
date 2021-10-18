from typing import TYPE_CHECKING

from db import Database
from vk_bot.core.search import GroupResult, TeacherResult

if TYPE_CHECKING:
    from vk_bot.core.search import AbstractResult


async def get_subscribes(chat_id: int) -> list['AbstractResult']:
    db = Database.from_keeper()

    subscribes = [GroupResult(i) for i in await db.get_user_subscriptions_group(chat_id)]
    subscribes += [TeacherResult(i) for i in await db.get_user_subscriptions_teacher(chat_id)]

    return subscribes


def get_notify_message(subscribes: list['AbstractResult']) -> str:
    message_lines = [
        'Для добавления подписки напишите номер группы/ФИО преподавателя.',
        'Для удаления подписки выберите её в меню или напишите номер группы/ФИО преподавателя.',
        '',
        'Текущие подписки:',
        *(i.title for i in subscribes)
    ]

    return '\n'.join(message_lines)
