import config
from vkbottle import Bot

bot = Bot(tokens=config.TOKEN_BOT, secret=config.SECRET)


if __name__ == '__main__':
    from routes import query_timetable, call_schedule, notify, other

    bot.set_blueprints(
        call_schedule.bp,
        notify.bp,
        other.bp,
        query_timetable.bp
    )
    bot.run_polling()
