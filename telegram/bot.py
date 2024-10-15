import asyncio

from aiogram import Bot, Dispatcher

from parser.downdetectorsu_parser import DownDetectorSuParser
from repo.mongo_repo import MongoRepo
from telegram.handlers import router
from repo.json_repo import JsonRepo

from config import BOT_TOKEN, MONGO_URI
from telegram.service_status_update import start_updating

bot = Bot(BOT_TOKEN)
dp = Dispatcher(repo=MongoRepo(MONGO_URI, "data"), parser=DownDetectorSuParser())
dp.include_router(router)


async def run() -> None:
    asyncio.ensure_future(start_updating(dp, bot))
    await dp.start_polling(bot)


