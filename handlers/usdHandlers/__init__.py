from aiogram import Dispatcher

from handlers.usdHandlers.user.start_handlers import register_all_start_handlers
from handlers.usdHandlers.user.main_menu_handlers import register_main_menu_handlers

def register_usdbot_handlers(dp: Dispatcher):
    register_all_start_handlers(dp)
    register_main_menu_handlers(dp)
