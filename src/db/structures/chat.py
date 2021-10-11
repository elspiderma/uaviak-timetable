from dataclasses import dataclass

from db.structures import DbObject


@dataclass
class Chat(DbObject):
    id: int
    vk_id: int
    timetable_photo: bool
