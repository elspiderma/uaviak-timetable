import os

from vkbottle.bot import Blueprint, Message

import config
from utils.photo_uploader import PhotoUploader

bp = Blueprint(name="Call schedule")
bp.vbml_ignore_case = True


@bp.on.message(text=['з', 'звонки'])
async def call_schedule(msg: Message):
    """Расписание звонков"""
    if not hasattr(call_schedule, 'uploader'):
        call_schedule.uploader = PhotoUploader(os.path.join(config.STATIC_DIR, 'schedule.jpg'), 'schedule', bp.api)

    await msg.answer(attachment=await call_schedule.uploader.id_photo, reply_to=msg.id)
