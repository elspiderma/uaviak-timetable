from uaviak_timetable import Timetable

from random import randint

from .base import CommandBase

from utils.text_creater import TextCreater

class TimetableGroupCommand(CommandBase):
    def check(self, event):
        return True

    @staticmethod
    def _gen_timetable_text(tt_group, group):
        text = TextCreater(f'Расписание группы {group}:')
        for lesson in tt_group:
            line = f'{lesson.number}) {lesson.cabinet} каб. {lesson.teacher} {lesson.subject}'
            if lesson.is_splitting:
                line += ' дрб'
            
            text.add(line)

        return str(text)

    def run(self, event):
        group = event['message']['text']

        tt = Timetable.load()
        tt_group = tt.find(group=group)

        if len(tt_group) == 0:
            self.vk.messages.send(peer_id=event['message']['peer_id'], message=f'Группа "{group}" не найдена!', random_id=randint(0, 9999999))
            return

        self.vk.messages.send(peer_id=event['message']['peer_id'], message=self._gen_timetable_text(tt_group, group), random_id=randint(0, 9999999))
