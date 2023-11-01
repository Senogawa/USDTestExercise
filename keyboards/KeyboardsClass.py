"""
Класс для хранения всех клавиатур бота
"""

from aiogram import types

class UsdKeyboards:
    mainKeyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    mainKeyboard.add("Узнать текущий курс")
    mainKeyboard.add("Подписаться на получение курса")
    mainKeyboard.add("История получения курса")

    mainKeyboardWithSub = types.ReplyKeyboardMarkup(resize_keyboard = True)
    mainKeyboardWithSub.add("Узнать текущий курс")
    mainKeyboardWithSub.add("Отписаться от получения курса")
    mainKeyboardWithSub.add("История получения курса")
