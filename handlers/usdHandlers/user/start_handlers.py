from aiogram import Dispatcher
from states.StatesClass import BotStates
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from keyboards.KeyboardsClass import UsdKeyboards



async def start_handler(message: types.Message):
    await message.answer(
        """
Привет!
С помощью этого бота Вы можете узнать текущий курс доллара.
        """,
        reply_markup = UsdKeyboards.mainKeyboard
    )


def register_all_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands = "start")