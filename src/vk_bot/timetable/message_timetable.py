from typing import TYPE_CHECKING, Optional

from vkbottle import PhotoMessageUploader

from db import Database
from vk_bot.keyboards import generate_keyboard_date
from vk_bot.timetable import TimetablePhoto, TimetableText

if TYPE_CHECKING:
    import datetime
    from vk_bot.search import AbstractResult
    from db.structures import TimetableForSomeone
    from vkbottle import API


async def _get_id_photo_timetable(api: 'API', timetable: 'TimetableForSomeone') -> str:
    cache_key = f'timetable_{timetable.date.isoformat()}_{timetable.whose_timetable.value}_{timetable.someone.id}'

    db = Database.from_keeper()

    cached_photo_id = await db.get_cache_photo_id_by_key(cache_key)
    if cached_photo_id:
        return cached_photo_id.vk_photo_id

    img = TimetablePhoto(timetable, 'NotoSans-Regular', 42).draw_photo_timetable()
    photo_id = await PhotoMessageUploader(api).upload(img)

    await db.set_cache_photo(cache_key, photo_id)
    return photo_id


async def get_message_timetable_for_result_search(
        api: 'API',
        chat_id: int,
        result: 'AbstractResult',
        date: 'datetime.date' = None
) -> tuple[str, Optional[str], str]:
    """Возвращает текст сообщения, фото и клавиатуру с датой для результата поиска.

    Args:
        api: # TODO
        chat_id: # TODO
        result: Результат поиска.
        date: Дата расписания, если None, то используется последняя дата.

    Returns:
        Текст расписания и клавиатура с доступными датами.
    """
    db = Database.from_keeper()
    chat = await db.get_chat_and_create_if_not_exist(chat_id)

    dates = await result.get_dates_timetable(9)

    # Если дата не передана, то используем последнию дату.
    if not date:
        date = dates[0]

    timetable = await result.get_timetable(date)

    kb = generate_keyboard_date(dates, date, timetable)

    if chat.timetable_photo:
        photo_id = await _get_id_photo_timetable(api, timetable)
        message = f'{timetable.someone.title}\n' \
                  f'{timetable.date.strftime("%a %d.%m")}'
    else:
        photo_id = None
        message = TimetableText(timetable).generate_text_timetable()

    return message, photo_id, kb.get_json()