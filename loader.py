from configparser import ConfigParser

cnf = ConfigParser()
cnf.read("botsConf.ini")

usdBotCnf = cnf["TELEGRAM"]
