from aiogram import Dispatcher
from states.StatesClass import BotStates
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from keyboards.KeyboardsClass import UsdKeyboards
from orm.usdBot.database_work import Database



async def start_handler(message: types.Message):

    database = Database("test_db.db")
    keyboard = UsdKeyboards.mainKeyboard

    if not database.check_user_in_database(message.from_id):
        database.add_user(message.from_id)

    if database.check_subscribe_for_notifications(message.from_id):
        keyboard = UsdKeyboards.mainKeyboardWithSub

    await message.answer(
        """
Привет!
С помощью этого бота Вы можете узнать текущий курс доллара.
        """,
        reply_markup = keyboard
    )

    await BotStates.main_menu.set()


def register_all_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands = "start")