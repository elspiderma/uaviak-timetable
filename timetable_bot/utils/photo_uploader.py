import json
import os
from typing import TYPE_CHECKING, NamedTuple, Union

import aiohttp

from db import session, CachePhoto

if TYPE_CHECKING:
    from vkbottle.types import Photo
    from vkbottle.api import Api


class PhotoUploader:
    """Кэширующий, загрузчик фото. Если фото уже залито на сервера VK, то не будет загружать повторно.

    TODO: Добавить возможность удаления фото из кэша.
    TODO: Сверять фото по дате изменения.
    """

    class PhotoUploadedInfo(NamedTuple):
        server: str
        photo: str
        hash: str

    def __init__(self, path: str, name_file: str, vk_api: 'Api'):
        self.path = path
        self.name_file = name_file
        self.content_type = self.get_content_type(path)
        self.vk = vk_api
        self.__id_photo: Union[str, None] = None

    @property
    async def id_photo(self):
        if self.__id_photo is None:
            await self._set_id_photo()

        return self.__id_photo

    def _get_cache(self):
        """Метод, получающий фото из кэша. Если фото не кэширавано, то возвращает `None`"""
        photo_cache: CachePhoto = session.query(CachePhoto).filter_by(name_file=self.name_file).first()
        if photo_cache:
            return photo_cache.id_vk

    def _save_cache(self):
        """Сохраняет фото в кэш"""
        cache_photo = CachePhoto(id_vk=self.__id_photo, name_file=self.name_file)
        session.add(cache_photo)
        session.commit()

    async def _set_id_photo(self) -> None:
        """Устанавливает атрибут `__id_photo`."""
        # Проверяем наличие фото в кеше
        cache_photo = self._get_cache()
        if cache_photo is not None:
            self.__id_photo = cache_photo
            return

        url = await self.__get_url_upload()
        uploaded_info = await self.__upload_to_server(url)
        saved_info = await self.__save_photo(uploaded_info)
        self.__id_photo = f'photo{saved_info.owner_id}_{saved_info.id}_{saved_info.access_key}'
        self._save_cache()

    @classmethod
    def __formation_id(cls, saved_info: 'Photo') -> str:
        """Формирует ID фото, для отправки в ЛС.
        Формат строки `photo{owner_id}_{photo_id}_{access_key}`.
        """
        return f'photo{saved_info.owner_id}_{saved_info.id}_{saved_info.access_key}'

    async def __save_photo(self, photo_info: PhotoUploadedInfo) -> 'Photo':
        """Сохроняет фото на серверах VK."""
        saved_info = await self.vk.photos.save_messages_photo(photo_info.photo, photo_info.server, photo_info.hash)
        return saved_info[0]

    async def __upload_to_server(self, url: str) -> PhotoUploadedInfo:
        """Загружает фото на сервер VK."""
        data = aiohttp.FormData()
        with open(self.path, 'rb') as f:
            data.add_field('photo',
                           f,
                           filename=os.path.split(self.path)[1],
                           content_type=self.content_type)

            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data) as resp:
                    photo_uploaded_info = await resp.text()
                    photo_uploaded_info = json.loads(photo_uploaded_info)

        return self.__class__.PhotoUploadedInfo(**photo_uploaded_info)

    async def __get_url_upload(self) -> str:
        """Получение ссылки на загрузку фото."""
        server_upload = await self.vk.photos.get_messages_upload_server()
        return server_upload.upload_url

    @classmethod
    def get_content_type(cls, path: str) -> str:
        """Определяет `content_type` для файла."""
        file_extension = os.path.splitext(path)[1]
        if file_extension == '.png':
            return 'image/png'
        elif file_extension in ('.jpg', '.jpeg'):
            return 'image/jpeg'
        elif file_extension == '.gif':
            return 'image/gif'
        else:
            raise Exception()