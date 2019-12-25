from uaviak_timetable import Timetable
from random import randint
from .base import CommandBase
from utils.text_creater import TextCreater

class TimetableGroupCommand(CommandBase):
    def check(self, event):
        if event['message']['text'][0:2] == 'г ':
            return True

        return False

    @classmethod
    def _gen_timetable_text(cls, tt_group, group):
        text = TextCreater()
        for lesson in tt_group:
            line = f'{lesson.number}) {lesson.cabinet} каб. {lesson.teacher} {lesson.subject}'
            types_string = cls._gen_type_lesson(lesson)
            if types_string is not None:
                line += ' ' + types_string
            
            text.add(line)

        return str(text)

    @staticmethod
    def _gen_type_lesson(lesson):
        types = list()

        if lesson.is_splitting:
            types.append('дроб.')
        if lesson.is_practice:
            types.append('прак.')
        if lesson.is_consultations:
            types.append('консулт.')

        if len(types) == 0:
            return None

        s = ', '.join(types)
        return f'({s})'

    def run(self, event):
        group = event['message']['text'].lower()[2:]

        tt = Timetable.load()
        tt_group = tt.find(group=group)

        if len(tt_group) == 0:
            self.vk.messages.send(peer_id=event['message']['peer_id'], message=f'Группа "{group}" не найдена!', random_id=randint(0, 9999999))
            return

        self.vk.messages.send(peer_id=event['message']['peer_id'], message=self._gen_timetable_text(tt_group, group), random_id=randint(0, 9999999))
