from aiogram import Dispatcher
from states.StatesClass import BotStates
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from keyboards.KeyboardsClass import UsdKeyboards
from aiohttp import ClientConnectorError

from middlewares.usdBotSoftware.usdCourse import get_usd_course
from orm.usdBot.database_work import Database



async def main_menu_handler(message: types.Message, state: FSMContext):
    database = Database("test_db.db")

    if message.text == "Узнать текущий курс":
        try:
            course = await get_usd_course()
            database.add_new_course_history(message.from_id, course)
            await message.answer(f"Текущий курс доллара: {course} RUB")

        except ClientConnectorError as ex:
            print(f"Ошибка {ex}")
            await message.answer("Ошибка получения курса, попробуйте позже")

        return

    if message.text == "Подписаться на получение курса":
        database.change_notifications_status(message.from_id, True)
        await message.answer("Вы подписались на переодическое получение курса доллара", reply_markup = UsdKeyboards.mainKeyboardWithSub)
        return

    if message.text == "Отписаться от получения курса":
        database.change_notifications_status(message.from_id, False)
        await message.answer("Вы отписались от переодического получения курса доллара", reply_markup = UsdKeyboards.mainKeyboard)
        return

    if message.text == "История получения курса":
        ...
        #TODO отправить inline сообщение
        return
    
    await message.answer("Нет такого варианта ответа")
    return
    

def register_main_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(main_menu_handler, state = BotStates.main_menu)