import os
import aiohttp
import json
from typing import NamedTuple
from vkbottle.types.responses.photos import GetMessagesUploadServer


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
