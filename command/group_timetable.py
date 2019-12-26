from uaviak_timetable import Timetable
from random import randint

from command.timetable import TimetableCommand
from utils.text_creater import TextCreater


class TimetableGroupCommand(TimetableCommand):
    def check(self, event):
        if event['message']['text'][0:2] == 'г ':
            return True

        return False

    @classmethod
    def _gen_lesson_text(cls, lesson):
        s = f'{lesson.number}) {lesson.cabinet} каб. {lesson.teacher} {lesson.subject}'
        type_str = cls._gen_type_lesson(lesson)

        if type_str is not None:
            s += f' {type_str}'

        return s


    def run(self, event):
        group = event['message']['text'].lower()[2:]

        tt = Timetable.load()
        tt_group = tt.find(group=group)

        if len(tt_group) == 0:
            self.vk.messages.send(peer_id=event['message']['peer_id'], message=f'Группа "{group}" не найдена!', random_id=randint(0, 9999999))
            return

        self.vk.messages.send(peer_id=event['message']['peer_id'], message=self._gen_timetable_text(tt_group, group), random_id=randint(0, 9999999))


# line = f'{lesson.number}) {lesson.cabinet} каб. {lesson.teacher} {lesson.subject}'
# types_string = cls._gen_type_lesson(lesson)
# if types_string is not None:
#     line += ' ' + types_string