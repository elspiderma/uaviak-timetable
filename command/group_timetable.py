from uaviak_timetable import Timetable
from random import randint

from command.timetable import TimetableCommand
from utils.text_creater import TextCreater


class TimetableGroupCommand(TimetableCommand):
    def check(self):
        text = self.event['message']['text'].lower()

        if text.startswith('г '):
            return True

        return False

    @classmethod
    def _gen_lesson_text(cls, lesson):
        s = f'{lesson.number}) {lesson.cabinet} каб. {lesson.teacher} {lesson.subject}'
        type_str = cls._gen_type_lesson(lesson)

        if type_str is not None:
            s += f' {type_str}'

        return s

    def run(self):
        group = self.event['message']['text'][2:].lower()

        tt = Timetable.load()
        tt_group = tt.find(group=group)

        if len(tt_group) == 0:
            m = f'Группа "{group}" не найдена!'
            self.vk.messages.send(peer_id=self.event['message']['peer_id'], message=m, random_id=randint(0, 9999999))
            return

        self.vk.messages.send(peer_id=self.event['message']['peer_id'], message=self._gen_timetable_text(tt_group, group), random_id=randint(0, 9999999))
