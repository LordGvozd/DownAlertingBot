from aiogram import Bot, Dispatcher

from parser.downdetectorsu_parser import DownDetectorSuParser
from telegram.handlers import router
from repo.json_repo import JsonRepo

from config import BOT_TOKEN, STORAGE_PATH

bot = Bot(BOT_TOKEN)
dp = Dispatcher(repo=JsonRepo(STORAGE_PATH), parser=DownDetectorSuParser())
dp.include_router(router)


def run() -> None:
    dp.run_polling(bot)


