from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import uaviak_parser


class TimetableExistError(Exception):
    """Такое расписание уже существует.
    """
    def __init__(self, timetable: 'uaviak_parser.structures.Timetable'):
        self.timetable = timetable
        super().__init__(f'Timetable {self.timetable.date} exist in DB.')
