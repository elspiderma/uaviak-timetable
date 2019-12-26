from .base import CommandBase
from random import randint
from utils.text_creater import TextCreater

class NotFoundCommand(CommandBase):
    def check(self):
        return True

    def run(self):
        m = \
        'Команда найдена\n' \
        'Для того чтобы получить расписание группы напишите:\n' \
        'г номер_группы\n\n' \
        'Для того чтобы получить расписание преподователя напишите:\n' \
        'п фамилия'

        self.vk.messages.send(peer_id=self.event['message']['peer_id'], message=m, random_id=randint(0, 9999999))
