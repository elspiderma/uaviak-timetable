from PIL import Pilloq
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.structures import TimetableForSomeone


class TimetablePhoto:
    def __init__(self, timetable: 'TimetableForSomeone'):
        self.timetable = timetable

    def generate(self):
        pass
