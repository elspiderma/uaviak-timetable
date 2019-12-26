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
        tt_group = Timetable()
        for lesson in tt:
            if lesson.group.startswith(group):
                tt_group.append_lesson(lesson)
        tt_group.sort('number')

        if len(tt_group) == 0:
            m = f'Группа "{group}" не найдена!'
            self.vk.messages.send(peer_id=self.event['message']['peer_id'], message=m, random_id=randint(0, 9999999))
            return

        list_group = tt_group.list('group')
        list_group.sort()

        m = TextCreater()
        for i in list_group:
            m.add(f'{i}:')
            m.add(*self._gen_timetable_text(tt_group.find(group=i)).lines, '\n')

        self.vk.messages.send(peer_id=self.event['message']['peer_id'], message=m, random_id=randint(0, 9999999))
