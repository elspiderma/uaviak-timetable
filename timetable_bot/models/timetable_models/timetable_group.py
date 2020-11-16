from typing import Union, TYPE_CHECKING

import db
from models.timetable_models.timetable import TimetableABCModel
from structures import Group
from utils.string import approximate_match

if TYPE_CHECKING:
    from structures import TimetableForGroup


class TimetableGroupModel(TimetableABCModel):
    async def get_timetable(self, group: Union[Group, int]) -> 'TimetableForGroup':
        return await self._get_timetable(group_id=group if isinstance(group, int) else group.id)

    @property
    async def _list(self):
        """Список всех групп."""
        return await self._get_orm_object(db.Group, 'title')

    @classmethod
    def _match_object(cls, query: str, group: 'db.Group', approximate: bool) -> bool:
        return (approximate_match(group.title, query, ['-', ' ']) and approximate) or \
            (group.title == query and not approximate)

    @classmethod
    async def _parse_orm_object(cls, group: 'db.Group') -> 'Group':
        return Group(id=group.id, title=group.title)
