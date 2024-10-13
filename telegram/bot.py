from aiogram import Bot, Dispatcher
from telegram.handlers import router

from config import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


def run() -> None:
    dp.run_polling(bot)


