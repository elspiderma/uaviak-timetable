from uaviak_timetable import Timetable
from random import randint

from command.timetable import TimetableCommand
from utils.text_creater import TextCreater


class TimetableTeacherCommand(TimetableCommand):
    def check(self):
        text = self.event['message']['text'].lower()

        if text.startswith('п '):
            return True

        return False

    @classmethod
    def _gen_lesson_text(cls, lesson):
        return f'{lesson.number}) {lesson.cabinet} каб. {lesson.group} {lesson.subject}'

    def run(self):
        teacher = self.event['message']['text'].lower()[2:]

        tt = Timetable.load()

        tt_teacher = Timetable()
        for lesson in tt:
            if lesson.teacher.lower().find(teacher) != -1:
                tt_teacher.append_lesson(lesson)
        tt_teacher.sort('number')

        if len(tt_teacher) == 0:
            self.vk.messages.send(peer_id=self.event['message']['peer_id'], message=f'Преподаватель "{teacher}" не найден!', random_id=randint(0, 9999999))
            return

        self.vk.messages.send(peer_id=self.event['message']['peer_id'], message=self._gen_timetable_text(tt_teacher, teacher), random_id=randint(0, 9999999))
