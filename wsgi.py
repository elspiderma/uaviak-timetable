import flask
from main import bot
import json
from vk_bot.types.long_poll.update_long_poll import GroupUpdateLongPoll

application = flask.Flask(__name__)


@application.route('/', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        update = json.loads(flask.request.get_data().decode('utf-8'))

        bot.process_new_update(GroupUpdateLongPoll.de_dict(update))
        return 'ok'
    else:
        flask.abort(403)


if __name__ == '__main__':
    application.run(host='0.0.0.0', port='5000')
