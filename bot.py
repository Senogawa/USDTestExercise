from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

from loader import usdBotCnf
from handlers.usdHandlers import register_usdbot_handlers
from middlewares.usdBotSoftware.schdule_newsletter import start_scheduler

from threading import Thread

usdBot = Bot(token = usdBotCnf["usdToken"])
usdDp = Dispatcher(usdBot, storage = MemoryStorage())

#TODO добавить проверку на наличие базы

register_usdbot_handlers(usdDp)
Thread(target = start_scheduler, args = (usdBot,), daemon = True).start()

async def bot_start_pooling():
    try:
        await usdDp.start_polling()
    finally:
        usdDp.storage.close()




if __name__ == "__main__":
    asyncio.run(bot_start_pooling())