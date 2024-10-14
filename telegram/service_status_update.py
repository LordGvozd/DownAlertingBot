import asyncio

from aiogram import Dispatcher

from parser.abstract_parser import AbstractDownDetectorParser
from repo.abstract_repo import AbstractRepo


def start_updating(dp: Dispatcher) -> None:
    asyncio.ensure_future(update_loop(dp))

async def update_loop(dp: Dispatcher) -> None:
    pass