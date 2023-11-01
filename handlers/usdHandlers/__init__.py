from aiogram import Dispatcher

from handlers.usdHandlers.user.start_handlers import register_all_start_handlers

def register_usdbot_handlers(dp: Dispatcher):
    register_all_start_handlers(dp)
