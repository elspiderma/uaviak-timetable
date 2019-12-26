from uaviak_timetable import Timetable
from random import randint

from command.timetable import TimetableCommand
from utils.text_creater import TextCreater


class TimetableGroupCommand(TimetableCommand):
    def check(self):
        return self._message_starts_with('г ')

    @classmethod
    def _gen_lesson_text(cls, lesson):
        return f'{lesson.number}) {lesson.cabinet} каб. {lesson.teacher} {lesson.subject}'

    def run(self):
        group = self.event['message']['text'][2:].lower()

        tt = Timetable.load()
        tt_group = tt.find(group=group)

        if len(tt_group) == 0:
            m = f'Группа "{group}" не найдена!'
            self.vk.messages.send(peer_id=self.event['message']['peer_id'], message=m, random_id=randint(0, 9999999))
            return

        self.vk.messages.send(peer_id=self.event['message']['peer_id'], message=self._gen_timetable_text(tt_group, group), random_id=randint(0, 9999999))
