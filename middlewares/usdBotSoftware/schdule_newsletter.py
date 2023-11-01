import schedule
from orm.usdBot.database_work import Database
from aiogram import Bot
from middlewares.usdBotSoftware.usdCourse import get_usd_course
import requests
import asyncio
from loader import usdBotCnf
import time
from logger_settings import logger

def send_notifications(bot: Bot):
    database = Database("test_db.db")
    users_with_notifications = database.get_users_with_notifications()

    if not len(users_with_notifications):
        logger.info("Нет подписавшихся пользователей")

    for user_id in users_with_notifications:
        course = asyncio.run(get_usd_course())
        requests.get(f"https://api.telegram.org/bot{usdBotCnf['usdToken']}/sendMessage?chat_id={user_id}&text=Текущий курс доллара: {course}")
        time.sleep(0.5)

        database.add_new_course_history(user_id, course)


def start_scheduler(bot: Bot):
    send_notifications(bot)
    schedule.every(1).minutes.do(send_notifications, bot)
    while True:
        schedule.run_pending()
        time.sleep(10)

if __name__ == "__main__":
    send_notifications(...)