import sys
import flask
from main import bot
import logging
import json
import threading

application = flask.Flask(__name__)


@application.route('/', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        update = json.loads(flask.request.get_data().decode('utf-8'))

        a = threading.Thread(target=bot.process_new_update, args=(update['type'], update['object'], ), daemon=True)
        a.start()
        return 'ok'
    else:
        flask.abort(403)


logging.basicConfig(stream=sys.stderr, level=logging.INFO)

if __name__ == '__main__':
    application.run(host='0.0.0.0', port='80')
