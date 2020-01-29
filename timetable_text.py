from uaviak_timetable import Timetable


def __get_text_type_lesson(lesson):
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


def __check_header_group(group: str, head_group: str):
    group = group.lower()
    head_group = head_group.lower()

    return group.startswith(head_group)


def is_exist_group(head_group):
    tt = Timetable.load()
    list_group = tt.list('group')

    find_groups = []
    for i in list_group:
        if __check_header_group(i, head_group):
            find_groups.append(i)

    return find_groups


def group(head_group, tt=None):
    if tt is None:
        tt = Timetable.load()

    tt_groups = Timetable()
    for lesson in tt:
        if lesson.group.lower().startswith(head_group.lower()):
            tt_groups.append_lesson(lesson)

    if len(tt_groups) == 0:
        return None

    tt_groups.sort('number')

    list_group = tt_groups.list('group')
    list_group.sort()

    text = ''
    for i in list_group:
        lessons = tt_groups.find(group=i)

        text += f'\n{i}: \n'
        for j in lessons:
            type_lesson = __get_text_type_lesson(j)
            text += f'{j.number}) {j.cabinet} каб. {j.teacher} {j.subject}'

            if type_lesson:
                text += f' {type_lesson}'

            text += '\n'

    return text.strip()


def teacher(head_teacher, tt=None):
    if tt is None:
        tt = Timetable.load()

    tt_teacher = Timetable()
    for lesson in tt:
        if lesson.teacher.lower().startswith(head_teacher.lower()):
            tt_teacher.append_lesson(lesson)

    if len(tt_teacher) == 0:
        return None

    tt_teacher.sort('number')

    list_teacher = tt_teacher.list('teacher')
    list_teacher.sort()

    text = ''
    for i in list_teacher:
        lessons = tt_teacher.find(teacher=i)

        text += f'\n{i}: \n'
        for j in lessons:
            type_lesson = __get_text_type_lesson(j)
            text += f'{j.number}) {j.cabinet} каб. {j.group} {j.subject}'

            if type_lesson:
                text += f' {type_lesson}'

            text += '\n'

    return text.strip()
