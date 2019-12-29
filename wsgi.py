import os, sys
import flask
from main import proc_event
from vk_api import VkApi
import logging
import config
import json

application = flask.Flask(__name__)


@application.route('/')
def index():
    flask.abort(403)


@application.route(config.WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        vk = VkApi(token=config.TOKEN, api_version='5.103')
        vk_api = vk.get_api()

        update = json.loads(flask.request.get_data().decode('utf-8')).get('object')
        proc_event(vk_api, update)
        return 'ok'
    else:
        flask.abort(403)


logging.basicConfig(stream=sys.stderr, level=logging.INFO)
