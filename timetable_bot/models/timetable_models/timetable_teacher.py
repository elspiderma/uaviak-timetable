from typing import Union, TYPE_CHECKING

import db
from models.timetable_models.timetable import TimetableABCModel
from structures import Teacher
from utils.string import approximate_match

if TYPE_CHECKING:
    from structures import TimetableForTeacher


class TimetableTeacherModel(TimetableABCModel):
    async def get_timetable(self, teacher: Union[Teacher, int]) -> 'TimetableForTeacher':
        return await self._get_timetable(teacher_id=teacher if isinstance(teacher, int) else teacher.id)

    @property
    async def _list(self):
        """Список всех учителей."""
        return await self._get_orm_object(db.Teacher, 'short_name')

    @classmethod
    def _match_object(cls, query: str, teacher: 'db.Teacher', approximate: bool) -> bool:
        return (approximate_match(teacher.short_name, query, ['.', ' ']) and approximate) or \
               (teacher.short_name == query and not approximate)

    @classmethod
    async def _parse_orm_object(cls, teacher: 'db.Teacher') -> 'Teacher':
        return Teacher(id=teacher.id, name=teacher.short_name, full_name=teacher.full_name)
