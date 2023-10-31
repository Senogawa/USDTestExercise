from configparser import ConfigParser
from middlewares.Dataclasses import Bot, Database

cnf = ConfigParser()
cnf.read("conf.ini")

bot_cnf = cnf["TELEGRAM"]
db_cnf = cnf["DATABASE"]

bot_info = Bot(
        bot_cnf["token"],
        bot_cnf["admin"]
)

db_info = Database(
        db_cnf["user"],
        db_cnf["password"],
        db_cnf["host"],
        int(db_cnf["port"]),
        db_cnf["db"],
)

del bot_cnf
del db_cnf