from aiogram import Dispatcher
from states.StatesClass import BotStates
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from keyboards.KeyboardsClass import UsdKeyboards
from aiohttp import ClientConnectorError

from middlewares.usdBotSoftware.usdCourse import get_usd_course



async def main_menu_handler(message: types.Message, state: FSMContext):
    if message.text == "Узнать текущий курс":
        try:
            course = await get_usd_course()
            await message.answer(f"Текущий курс доллара: {course} RUB")

        except ClientConnectorError as ex:
            print(f"Ошибка {ex}")
            await message.answer("Ошибка получения курса, попробуйте позже")

        return

    if message.text == "Подписаться на получение курса":
        ...
        #TODO Изменить у пользователя в базе значение получение курса на True
        return

    if message.text == "История получения курса":
        ...
        #TODO отправить inline сообщение
        return
    
    await message.answer("Нет такого варианта ответа")
    return
    

def register_main_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(main_menu_handler, state = BotStates.main_menu)