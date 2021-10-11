from dataclasses import dataclass

from db.structures import DbObject


@dataclass
class VKCachePhoto(DbObject):
    id: int
    key_cache: str
    vk_photo_id: str
