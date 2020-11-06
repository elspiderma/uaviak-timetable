from vkbottle import Bot

import config

bot = Bot(tokens=config.TOKEN_BOT)

if __name__ == '__main__':
    from routes import query_timetable, call_schedule, notify, other

    bot.set_blueprints(
        call_schedule.bp,
        notify.bp,
        other.bp,
        query_timetable.bp
    )
    bot.run_polling()
