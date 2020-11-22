import db
from typing import List, Union
from structures import Teacher, Group


class Chat:
    def __init__(self, id_db, id_vk, is_photo):
        self.id_db = id_db
        self.id_vk = id_vk
        self.is_photo = is_photo
        self.is_private_message = id_vk < 2000000000

    @classmethod
    async def get_by_id(cls, id_vk: int) -> 'Chat':
        """Получает пользователя по ID Вконакте.

        @param id_vk: ID ВК.
        @return: Объект пользователя.
        """
        chat_db = await db.Chat.filter(id_vk=id_vk).first()
        if chat_db is None:
            chat_db = await db.Chat.create(id_vk=id_vk)

        return cls(chat_db.id, chat_db.id_vk, chat_db.is_photo)

    async def subscribe_notify(self, subscription: Union['Teacher', 'Group']):
        """Подписывает пользователя на рассылку расписания.

        @param subscription: Группа или преподаватель для рассылки.
        """
        if isinstance(subscription, Teacher):
            await db.NotifyTeacher.create(chat_id=self.id_db, teacher_id=subscription.id)
        else:
            await db.NotifyGroup.create(chat_id=self.id_db, group_id=subscription.id)

    async def unsubscribe_notify(self, subscription: Union['Teacher', 'Group']):
        """Отписывает пользователя от рассылки.

        @param subscription: Группа или преподаватель для отписки.
        """
        if isinstance(subscription, Teacher):
            await db.NotifyTeacher.filter(chat_id=self.id_db, teacher_id=subscription.id).delete()
        else:
            await db.NotifyGroup.filter(chat_id=self.id_db, group_id=subscription.id).delete()

    async def is_subscribe_notify(self, subscription: Union['Teacher', 'Group']) -> bool:
        """Проверяет, есть ли у пользователя подпска.

        @param subscription: Группа или преподаватель рассылку которого надо проверить.
        @return: True - если подписка есть, иначе False.
        """
        if isinstance(subscription, Teacher):
            return await db.NotifyTeacher.filter(chat_id=self.id_db, teacher_id=subscription.id).exists()
        else:
            return await db.NotifyGroup.filter(chat_id=self.id_db, group_id=subscription.id).exists()

    async def list_notify(self) -> List[Union['Teacher', 'Group']]:
        # TODO: Список подписок.
        pass
