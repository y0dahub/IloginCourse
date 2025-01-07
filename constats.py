from aiogram import Bot, Dispatcher
from config import TOKEN

from data.database import Database
from config import DB_DATA

BOT = Bot(TOKEN)
DP = Dispatcher()
DB = Database(user=DB_DATA.get("user"),
              password=DB_DATA.get("password"),
              host=DB_DATA.get("host"),
              database_name=DB_DATA.get("database_name"))

INTERESTS = ["python", "c++", "java", "kotlin", "go", "front end", "c#"]