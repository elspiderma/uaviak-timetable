import os
import random
import json
from typing import Tuple, NamedTuple
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


class PhotoInfo(NamedTuple):
    server: str
    photo: str
    hash: str


async def upload_photo(upload_server: GetMessagesUploadServer, path: str) -> PhotoInfo:
    if not os.path.isfile(path):
        raise FileNotFoundError

    def get_content_type():
        file_extension = os.path.splitext(path)[1]
        if file_extension == '.png':
            return 'image/png'
        elif file_extension in ('.jpg', '.jpeg'):
            return 'image/jpeg'
        elif file_extension == '.gif':
            return 'image/gif'
        else:
            raise Exception()

    url = upload_server.upload_url

    data = aiohttp.FormData()
    data.add_field('photo',
                   open(path, 'rb'),
                   filename=os.path.split(path)[1],
                   content_type=get_content_type())

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            data_photo_upload = await resp.text()
            data_photo_upload = json.loads(data_photo_upload)

    return PhotoInfo(**data_photo_upload)


def parse_massive_int_env(name: str, sep: str = ',') -> Tuple[int]:
    varenv = os.getenv(name)
    if varenv is None:
        return tuple()

    varenv_split = varenv.split(sep)
    varenv_split = tuple(varenv_split)
    # Convert ('123', '345') to (123, 345)
    varenv_split = tuple(map(int, varenv_split))
    return varenv_split
