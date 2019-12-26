from uaviak_timetable import Timetable
from random import randint

from command.timetable import TimetableCommand
from utils.text_creater import TextCreater


class TimetableTeacherCommand(TimetableCommand):
    def check(self):
        return self._message_starts_with('п ')

    @classmethod
    def _gen_lesson_text(cls, lesson):
        return f'{lesson.number}) {lesson.cabinet} каб. {lesson.group} {lesson.subject}'

    def run(self):
        teacher = self.event['message']['text'].lower()[2:]

        tt = Timetable.load()

        tt_teacher = Timetable()
        for lesson in tt:
            if lesson.teacher.lower().startswith(teacher):
                tt_teacher.append_lesson(lesson)
        tt_teacher.sort('number')

        if len(tt_teacher) == 0:
            self.vk.messages.send(peer_id=self.event['message']['peer_id'], message=f'Преподаватель "{teacher}" не найден!', random_id=randint(0, 9999999))
            return

        list_teacher = tt_teacher.list('teacher')
        list_teacher.sort()

        m = TextCreater()
        for i in list_teacher:
            m.add(f'{i}:')
            m.add(*self._gen_timetable_text(tt_teacher.find(teacher=i)).lines, '\n')

        self.vk.messages.send(peer_id=self.event['message']['peer_id'], message=m, random_id=randint(0, 9999999))
