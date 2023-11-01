from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

from loader import usdBotCnf
from handlers.usdHandlers import register_usdbot_handlers

usdBot = Bot(token = usdBotCnf["usdToken"])
usdDp = Dispatcher(usdBot, storage = MemoryStorage())

register_usdbot_handlers(usdDp)

async def bot_start_pooling():
    try:
        await usdDp.start_polling()
    finally:
        usdDp.storage.close()




if __name__ == "__main__":
    asyncio.run(bot_start_pooling())