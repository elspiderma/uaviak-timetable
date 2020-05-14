import os
import config
from utils import upload_photo
from vkbottle.bot import Blueprint, Message

bp = Blueprint(name="Call schedule")


@bp.on.message(text=['з', 'звонки'])
async def call_schedule(msg: Message):
    upload_server = await msg.api.photos.get_messages_upload_server()
    photo_info = await upload_photo(upload_server, os.path.join(config.STATIC_DIR, 'schedule.jpg'))

    loaded_photo = await msg.api.photos.save_messages_photo(photo_info.photo, photo_info.server, photo_info.hash)
    id_photo = f'photo{loaded_photo[0].owner_id}_{loaded_photo[0].id}_{loaded_photo[0].access_key}'

    await msg(attachment=id_photo, reply_to=msg.id)
