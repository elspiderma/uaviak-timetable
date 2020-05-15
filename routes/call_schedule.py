import os
import config
from utils.photo_uploader import PhotoUploader
from vkbottle.bot import Blueprint, Message

bp = Blueprint(name="Call schedule")


@bp.on.message(text=['з', 'звонки'], lower=True)
async def call_schedule(msg: Message):
    if not hasattr(call_schedule, 'uploader'):
        call_schedule.uploader = PhotoUploader(os.path.join(config.STATIC_DIR, 'schedule.jpg'), 'schedule', msg.api)

    await msg(attachment=await call_schedule.uploader.id_photo, reply_to=msg.id)
