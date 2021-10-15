from db.structures import TypesLesson, WhoseTimetable

TYPES_TO_STRING: dict[TypesLesson, str] = {
    TypesLesson.EXAM: 'экз',
    TypesLesson.SPLIT: 'дрб',
    TypesLesson.PRACTICAL: 'практ',
    TypesLesson.CONSULTATION: 'конс'
}

WHOSE_TIMETABLE_TO_STRING: dict[WhoseTimetable, str] = {
    WhoseTimetable.FOR_TEACHER: 'Преподаватель',
    WhoseTimetable.FOR_GROUP: 'Группа'
}
