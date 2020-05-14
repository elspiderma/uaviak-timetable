import os
import random
import json
from typing import Tuple

from vkbottle.types.responses.photos import GetMessagesUploadServer
import aiohttp


def number_weekday_to_text(number: int) -> str:
    if number == 0:
        return 'Пн'
    elif number == 1:
        return 'Вт'
    elif number == 2:
        return 'Ср'
    elif number == 3:
        return 'Чт'
    elif number == 4:
        return 'Пт'
    elif number == 5:
        return 'Сб'
    elif number == 6:
        return 'Вс'


def get_random() -> int:
    return random.getrandbits(31) * random.choice([-1, 1])


async def upload_photo(upload_server: GetMessagesUploadServer, path) -> Tuple[str, str, str]:
    url = upload_server.upload_url

    file_extension = os.path.splitext(path)[1]
    if file_extension == '.png':
        content_type = 'image/png'
    elif file_extension in ('.jpg', '.jpeg'):
        content_type = 'image/jpeg'
    elif file_extension == '.gif':
        content_type = 'image/gif'
    else:
        raise Exception()

    data = aiohttp.FormData()
    data.add_field('photo',
                   open(path, 'rb'),
                   filename=os.path.split(path)[1],
                   content_type=content_type)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            data_photo_upload = await resp.text()
            data_photo_upload = json.loads(data_photo_upload)

    return data_photo_upload['server'], data_photo_upload['photo'], data_photo_upload['hash']


def parse_massive_int_env(name: str, sep: str = ',') -> Tuple[int]:
    varenv = os.getenv(name)
    if varenv is None:
        return tuple()

    varenv_split = varenv.split(sep)
    varenv_split = tuple(varenv_split)
    # Convert ('123', '345') to (123, 345)
    varenv_split = tuple(map(int, varenv_split))
    return varenv_split
