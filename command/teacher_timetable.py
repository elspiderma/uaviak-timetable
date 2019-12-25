from uaviak_timetable import Timetable
from random import randint
from .base import CommandBase
from utils.text_creater import TextCreater
import re
from command.group_timetable import TimetableGroupCommand

class TimetableTeacherCommand(TimetableGroupCommand):
    def check(self, event):
        if event['message']['text'][0:2] == 'п ':
            return True

        return False

    def run(self, event):
        teacher = event['message']['text'].lower()[2:]
        teacher = re.escape(teacher)

        tt = Timetable.load()

        tt_teacher = Timetable()
        for lesson in tt:
            if re.search(rf'{teacher}', lesson.teacher, re.IGNORECASE):
                tt_teacher.append_lesson(lesson)

        tt_teacher.sort('number')

        if len(tt_teacher) == 0:
            self.vk.messages.send(peer_id=event['message']['peer_id'], message=f'Преподаватель "{teacher}" не найден!', random_id=randint(0, 9999999))
            return

        self.vk.messages.send(peer_id=event['message']['peer_id'], message=self._gen_timetable_text(tt_teacher, teacher), random_id=randint(0, 9999999))
