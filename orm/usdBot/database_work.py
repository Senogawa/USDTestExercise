from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, select, update, Table, Column, Integer, String 
from orm.usdBot.models import base
from logger_settings import logger
import time
import numpy as np
from sqlalchemy.exc import OperationalError


class Database:
    def __init__(self, database_name: str): #TODO добавить конфиг файл
        """
        Работает с sqlite
        """

        self.engine = create_engine(f"sqlite:///{database_name}")
        self.meta = MetaData()
        self.meta.reflect(self.engine)
        
        if "users" not in self.meta.tables:
            base.metadata.create_all(self.engine)
            logger.info("Была создана таблица users")

    def add_user(self, user_id: int):
        """
        Добавление пользователя в базу данных
        """

        conn = self.engine.connect()
        with self.engine.connect() as conn:
            users = Table("users", self.meta)
            query = insert(users).values(user_id = user_id, notifications = False)
            #print(query)
            conn.execute(query)
            conn.commit()
            logger.info(f"Добавлен пользователь {user_id}")

    def check_user_in_database(self, user_id: int) -> bool:
        """
        Проверка наличия пользователя в базе данных
        """

        with self.engine.connect() as conn:
            users = Table("users", self.meta)
            query = select(users).where(users.c.user_id == user_id)
            result = conn.execute(query).fetchall()
            
            if len(result) == 0:
                return False
            
            return True


    def change_notifications_status(self, user_id:int, notifications_status: bool):
        """
        Изменение статуса получения рассылки
        """

        with self.engine.connect() as conn:
            users = Table("users", self.meta)
            query = update(users).where(users.c.user_id == user_id).values(notifications = notifications_status)

            conn.execute(query)
            conn.commit()

            logger.info(f"Состояние подписки {user_id} обновлено на {notifications_status}")

    def check_subscribe_for_notifications(self, user_id: int) -> bool:
        """
        Проверка на наличие подписки для рассылки
        """

        with self.engine.connect() as conn:
            users = Table("users", self.meta)
            query = select(users).where(users.c.user_id == user_id)

            result = conn.execute(query).fetchall()
            if result[0][2]:
                return True
            
            return False

    def get_users_with_notifications(self) -> list:
        """
        Получение списка пользователей с включенной рассылкой
        """

        with self.engine.connect() as conn:
            users = Table("users", self.meta)

            query_for_check_users_count = select(users)
            try:
                users_count = len(conn.execute(query_for_check_users_count).fetchall())

            except OperationalError:
                return list()

            if not users_count:
                return list()

            query = select(users).where(users.c.notifications == True)

            result = conn.execute(query).fetchall()
            result = [user[1] for user in result]
            
        return result



    def add_new_course_history(self, user_id: int, course: str):
        """
        Добавление новой записи о получении курса
        """

        with self.engine.connect() as conn:
            if f"{user_id}_courses" not in self.meta.tables: #Если таблица не существует
                users_table = Table(
                    f"{user_id}_courses",
                    self.meta,
                    Column("id", Integer, primary_key = True),
                    Column("timestamp", Integer, nullable = True),
                    Column("value", String, nullable = True)
                )

                users_table.create(conn)
                
            users_table = Table(f"{user_id}_courses", self.meta)
            query = insert(users_table).values(timestamp = int(time.time()), value = course)

            conn.execute(query)
            conn.commit()
            logger.info(f"История получения курса для пользователя {user_id} обновлена")


    def get_course_history(self, user_id: int) -> list:
        """
        Получение истории запросов курса у конкретного пользователя
        """

        with self.engine.connect() as conn:
            if f"{user_id}_courses" not in self.meta.tables:
                return list()

            users_table = Table(f"{user_id}_courses", self.meta)
            query = select(users_table)
            result = conn.execute(query).fetchall()
            
        reversed_result = sorted(result, reverse = True)

        courses_history = list()

        if len(reversed_result) == 0:
            return courses_history

        if len(reversed_result) <= 5:
            courses_history.append(reversed_result)
            return courses_history
        
        course_page = list()
        while True:
            if len(reversed_result) > 5:
                for i in range(0, 5):
                    course_page.append(reversed_result[i])
                    #print(course_page)

                courses_history.append(course_page)
                #print(courses_history)

                for i in range(0, 5):
                    reversed_result.pop(0)

                course_page = list()

            if len(reversed_result) <= 5 and len(reversed_result) != 0:
                courses_history.append(reversed_result)
                break

            if len(reversed_result) == 0:
                break

        return courses_history
        



#database = Database("test_db.db")

def __main():
    database = Database("test_db.db")
    #database.add_new_course_history(111122, "93.76")
    print(database.get_course_history(1081181910))
    #print(database.check_user_in_database(11112))
    #print(database.get_users_with_notifications())
    #print(database.check_subscribe_for_notifications(1081181910))

if __name__ == "__main__":
    __main()