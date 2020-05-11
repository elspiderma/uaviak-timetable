import os

TOKEN_BOT = os.getenv('TOKEN_BOT')
CONFIRMATION_TOKEN = os.getenv('CONFIRMATION_TOKEN')
SECRET = os.getenv('SECRET')

DATA_BASE = os.getenv('DATA_BASE')

STATIC_DIR = os.getenv('STATIC_DIR', f'{os.path.dirname(__file__)}/static')
