"""
Класс для хранения состояний бота
"""

from aiogram.dispatcher.filters.state import StatesGroup, State

class BotStates(StatesGroup):
    main_menu = State()
    