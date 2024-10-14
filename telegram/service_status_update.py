import asyncio

from aiogram import Dispatcher, Bot

import config
from config import UPDATE_TIME
from models import ServiceStatus
from parser.abstract_parser import AbstractDownDetectorParser
from repo.abstract_repo import AbstractRepo


def start_updating(dp: Dispatcher, bot: Bot) -> None:
    asyncio.ensure_future(update_loop(dp, bot))

async def update_loop(dp: Dispatcher, bot: Bot) -> None:
    # Wait, while bot and dp would fully load
    await asyncio.sleep(5)

    repo: AbstractRepo = dp["repo"]
    parser: AbstractDownDetectorParser = dp["parser"]

    while True:
        old_state = repo.get_services_state()
        new_state = parser.get_problems_services()

        services_to_alert = []

        # Find diff
        for s in new_state:
            if s not in old_state:
                services_to_alert.append(s)

        repo.save_services_state(new_state)

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

        # Send broadcast
        for u in repo.get_all_users():
            await bot.send_message(u, answer_text)

        # Wait
        await asyncio.sleep(UPDATE_TIME)