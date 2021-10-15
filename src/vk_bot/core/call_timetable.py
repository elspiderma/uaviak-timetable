from typing import TYPE_CHECKING

from vkbottle import PhotoMessageUploader

from config import ConfigurationKeeper
from db import Database

if TYPE_CHECKING:
    from vkbottle import API


async def get_photo_id_call_timetable(api: 'API') -> str:
    cache_key = 'call_timetable_photo'

    db = Database.from_keeper()
    cached_photo = await db.get_cache_photo_id_by_key(cache_key)

    if cached_photo:
        return cached_photo.vk_photo_id

    config = ConfigurationKeeper.get_configuration()
    photo_path = config.vk_bot_photo_call_timetable

    photo_id = await PhotoMessageUploader(api).upload(photo_path)
    await db.set_cache_photo(cache_key, photo_id)
    return photo_id
