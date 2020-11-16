import locale
import logging
import os

from utils.env import parse_massive_int_env, LOGGING_LEVEL

TOKEN_BOT = os.getenv('TOKEN_BOT')
DATA_BASE = os.getenv('DATA_BASE')

STATIC_DIR = os.getenv('STATIC_DIR', f'{os.path.dirname(__file__)}/static')
TMPDIR = os.getenv('TMPDIR', '/tmp')
if not os.path.isdir(TMPDIR):
    os.mkdir(TMPDIR)

ADMIN_ID = parse_massive_int_env('ADMIN_ID')

locale.setlocale(locale.LC_ALL, os.getenv('LANG'))

LOG_LEVEL = int(os.getenv('LOG_LEVEL', '3'))
logging.basicConfig(level=LOGGING_LEVEL[LOG_LEVEL])

TORTOISE_ORM = {
    "connections": {"default": DATA_BASE},
    "apps": {
        "models": {
            "models": ["db"],
            "default_connection": "default",
        },
    },
}
