import os

from utils.env import parse_massive_int_env

TOKEN_BOT = os.getenv('TOKEN_BOT')
DATA_BASE = os.getenv('DATA_BASE')

STATIC_DIR = os.getenv('STATIC_DIR', f'{os.path.dirname(__file__)}/static')
ADMIN_ID = parse_massive_int_env('ADMIN_ID')

TMPDIR = os.getenv('TMPDIR', '/tmp')
if not os.path.isdir(TMPDIR):
    os.mkdir(TMPDIR)
