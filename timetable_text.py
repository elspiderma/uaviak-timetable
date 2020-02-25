from uaviak_timetable import Timetable, Lesson
from utils import number_weekday_to_text


class TimetableText:
    def __init__(self, timetable=None):
        self.timetable = timetable
        if self.timetable is None:
            self.timetable = Timetable.load()
            self.timetable.sort('number')

    @classmethod
    def __get_text_type_lesson(cls, lesson):
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

    @classmethod
    def __del_unnecessary_chars(cls, group_name: str):
        group_name = group_name.lower()
        group_name = group_name.replace('-', '')
        group_name = group_name.replace(' ', '')
        return group_name

    @classmethod
    def __check_header_group(cls, group: str, head_group: str):
        group = cls.__del_unnecessary_chars(group)
        head_group = cls.__del_unnecessary_chars(head_group)

        return group.startswith(head_group)

    @classmethod
    def __get_text_lesson(cls, lesson: Lesson, attr: str):
        if attr == 'group':
            group_or_teacher = lesson.teacher
        else:
            group_or_teacher = lesson.group

        text = f'{lesson.number}) {lesson.cabinet} каб. {group_or_teacher} {lesson.subject}'
        group_type = cls.__get_text_type_lesson(lesson)

        if group_type is not None:
            text += group_type

        return text

    def __get_text(self, head_str, attr):
        text_attr = {}
        for lesson in self.timetable:
            value_attr = getattr(lesson, attr)
            if not self.__check_header_group(value_attr, head_str):
                continue

            if value_attr not in text_attr:
                text_attr[value_attr] = []

            text_attr[value_attr].append(self.__get_text_lesson(lesson, attr))

        if len(text_attr) == 0:
            return None

        text = ''
        for group_number in sorted(text_attr):
            text += f'{group_number}:\n'
            text += '\n'.join(text_attr[group_number])
            text += '\n\n'

        date_text = self.timetable.date.strftime('%d.%m')
        date_text = f'{number_weekday_to_text(self.timetable.date.weekday())} {date_text}'

        text += date_text

        return text

    def get_text_teacher(self, head_teacher):
        return self.__get_text(head_teacher, 'teacher')

    def get_text_group(self, head_group):
        return self.__get_text(head_group, 'group')

    def get_list_group(self, head_group):
        list_group = self.timetable.list('group')

        find_groups = []
        for i in list_group:
            if self.__check_header_group(i, head_group):
                find_groups.append(i)

        return find_groups

    def get_list_teacher(self, head_teacher):
        list_teachers = self.timetable.list('teacher')

        find_teachers = []
        for i in list_teachers:
            if self.__check_header_group(i, head_teacher):
                find_teachers.append(i)

        return find_teachers
