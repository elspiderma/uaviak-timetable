from vkbottle import Bot, LoopWrapper, BotPolling

import config
import db
import routes


async def startup():
    await db.init()


async def shutdown():
    await db.stop()


loopw = LoopWrapper()
loopw.on_startup.append(startup())
loopw.on_shutdown.append(shutdown())

bot_polling = BotPolling(wait=90)

bot = Bot(config.TOKEN_BOT, loop_wrapper=loopw, polling=bot_polling)

routes.bp_call_schedule.load(bot)
routes.bp_other.load(bot)
routes.bp_notify.load(bot)
routes.bp_query_timetable.load(bot)


if __name__ == '__main__':
    bot.run_forever()
