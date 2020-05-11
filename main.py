import config
from vkbottle import Bot
from routes import query_timetable, call_schedule, notify, other

bot = Bot(tokens=config.TOKEN_BOT, secret=config.SECRET)
bot.set_blueprints(
    call_schedule.bp,
    notify.bp,
    other.bp,
    query_timetable.bp
)

if __name__ == '__main__':
    bot.run_polling()
