from uaviak_timetable.timetable import Timetable as TimetableBase
import aiohttp
import db
from hashlib import sha256
import typing


class TimetableCache(TimetableBase):
    NAME_FIELD_HASH = 'HashHtmlTimetable'

    @classmethod
    def update_hash(cls, new_hash: str) -> bool:
        saved_hash: db.KeyValue = db.session.query(db.KeyValue).filter_by(name=cls.NAME_FIELD_HASH).first()
        if not saved_hash:
            db.session.add(db.KeyValue(name=cls.NAME_FIELD_HASH, value=new_hash))
            db.session.commit()
            return True

        if saved_hash.value == new_hash:
            return False
        else:
            saved_hash.value = new_hash
            db.session.commit()
            return True

    @classmethod
    async def load_from_site_if_updated(cls) -> typing.Optional['TimetableCache']:
        async with aiohttp.ClientSession() as aiohttp_session:
            response = await aiohttp_session.get(cls.URL_TIMETABLE)
            html = await response.text()
            hash_html = sha256(html.encode('UTF-8')).hexdigest()

            is_update = cls.update_hash(hash_html)

            return cls._parse_html_timetable(html) if is_update else None

