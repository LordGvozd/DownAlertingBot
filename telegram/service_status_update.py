import asyncio

from aiogram import Dispatcher, Bot

import config
from config import UPDATE_TIME
from models import ServiceStatus
from parser.abstract_parser import AbstractDownDetectorParser
from repo.abstract_repo import AbstractRepo


async def start_updating(dp: Dispatcher, bot: Bot) -> None:
    await update_loop(dp, bot)

async def update_loop(dp: Dispatcher, bot: Bot) -> None:
    # Wait, while bot and dp would fully load
    await asyncio.sleep(3)

    repo: AbstractRepo = dp["repo"]
    parser: AbstractDownDetectorParser = dp["parser"]

    while True:
        old_state = await repo.get_services_state()
        new_state = parser.get_problems_services()


        services_to_alert = []
        print(old_state)
        # Find diff
        for s in new_state:
            if s not in old_state:
                print(s)
                services_to_alert.append(s)

        asyncio.ensure_future(repo.save_services_state(new_state))

        answer_text = ""

        status_smail = ""
        for s in services_to_alert:
            match s.problem_status:
                case ServiceStatus.OK:
                    status_smail = "🟢"
                case ServiceStatus.WARNING:
                    status_smail = "🟡"
                case ServiceStatus.ERROR:
                    status_smail = "🔴"

            answer_text += f"{status_smail} {s.service_name}\n"

        if not answer_text:
            # Wait
            await asyncio.sleep(UPDATE_TIME * 60)
            continue

        # Send broadcast
        for u in await repo.get_all_users():
            await bot.send_message(u, answer_text)

        # Wait
        await asyncio.sleep(UPDATE_TIME * 60)