from aiogram import Dispatcher
from states.StatesClass import BotStates
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from keyboards.KeyboardsClass import UsdKeyboards
from aiohttp import ClientConnectorError

from middlewares.usdBotSoftware.usdCourse import get_usd_course
from orm.usdBot.database_work import Database
import time



async def next_page(query: types.CallbackQuery):
    database = Database("test_db.db")
    courses_history = database.get_course_history(query.from_user.id)
    len_indexes_courses_history = len(courses_history) - 1
    callback_data = query.data.split(':')

    if callback_data[1] == callback_data[2]:

        text_message = ""
        for course in courses_history[int(callback_data[1])]:
            gm_time = time.gmtime(course[1])
            text_message += f"Курс доллара {course[2]} | {time.strftime('%B %d %Y %H:%M:%S', gm_time)}\n"

        inline_keyboard = types.InlineKeyboardMarkup(1).add(
            types.InlineKeyboardButton("<-", callback_data = f"prev:{len_indexes_courses_history - 1}:{len_indexes_courses_history}")
        )

    else:
        text_message = ""
        for course in courses_history[int(callback_data[1])]:
            gm_time = time.gmtime(course[1])
            text_message += f"Курс доллара {course[2]} | {time.strftime('%B %d %Y %H:%M:%S', gm_time)}\n"

        inline_keyboard = types.InlineKeyboardMarkup(2).add(
            types.InlineKeyboardButton("<-", callback_data = f"prev:{int(callback_data[1])}:{len_indexes_courses_history}"),
            types.InlineKeyboardButton("->", callback_data = f"next:{int(callback_data[1]) + 1}:{len_indexes_courses_history}")
        )

    await query.message.edit_text(text_message, reply_markup = inline_keyboard)
    return

async def previous_page(query: types.CallbackQuery):
    database = Database("test_db.db")
    courses_history = database.get_course_history(query.from_user.id)
    len_indexes_courses_history = len(courses_history) - 1
    callback_data = query.data.split(':')
    #print(callback_data)

    if int(callback_data[1]) == 0:

        text_message = ""
        for course in courses_history[int(callback_data[1])]:
            gm_time = time.gmtime(course[1])
            text_message += f"Курс доллара {course[2]} | {time.strftime('%B %d %Y %H:%M:%S', gm_time)}\n"

        inline_keyboard = types.InlineKeyboardMarkup(1).add(
            types.InlineKeyboardButton("->", callback_data = f"next:1:{len_indexes_courses_history}")
        )

    else:
        text_message = ""
        for course in courses_history[int(callback_data[1])]:
            gm_time = time.gmtime(course[1])
            text_message += f"Курс доллара {course[2]} | {time.strftime('%B %d %Y %H:%M:%S', gm_time)}\n"

        inline_keyboard = types.InlineKeyboardMarkup(2).add(
            types.InlineKeyboardButton("<-", callback_data = f"prev:{int(callback_data[1]) - 1}:{len_indexes_courses_history}"),
            types.InlineKeyboardButton("->", callback_data = f"next:{int(callback_data[1])}:{len_indexes_courses_history}")
        )

    await query.message.edit_text(text_message, reply_markup = inline_keyboard)
    
    return

def register_course_history_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(next_page, text_startswith = "next", state = BotStates.main_menu)
    dp.register_callback_query_handler(previous_page, text_startswith = "prev", state = BotStates.main_menu)