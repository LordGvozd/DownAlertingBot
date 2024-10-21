import asyncio
import time
from datetime import datetime, timedelta

import aiogram.exceptions
from aiogram import Dispatcher, Bot
from loguru import logger

import config
from config import UPDATE_TIME
from schemas import ServiceStatus, ServiceInfo
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
        old_services = await repo.get_services_state()
        new_problems_services = parser.get_problems_services()

        updated_services = new_problems_services
        services_to_alert = []


        # Find diff
        for s in new_problems_services:
            if s not in old_services:
                services_to_alert.append(s)



        for service in old_services:
            if (not service.service_name in [n.service_name for n in new_problems_services]
                    and
                    service.service_status != ServiceStatus.OK):

                ok_service = ServiceInfo(
                    service_name=service.service_name,
                    service_status=ServiceStatus.OK
                )

                updated_services.append(ok_service)
                services_to_alert.append(ok_service)

        # Save changes to repo
        asyncio.ensure_future(repo.save_services_state(updated_services))

        # Sort services in alphabet order
        services_to_alert.sort(key=lambda x: x.service_name.lower())



        answer_text = ""

        status_smail = ""
        for s in services_to_alert:
            match s.service_status:
                case ServiceStatus.OK:
                    status_smail = "🟢"
                case ServiceStatus.WARNING:
                    status_smail = "🟡"
                case ServiceStatus.ERROR:
                    status_smail = "🔴"

            answer_text += f"{status_smail} {s.service_name}\n"

        if not answer_text:
            logger.debug("New services not exist")
            # Wait
            await asyncio.sleep(UPDATE_TIME * 60)
            continue

        # Send broadcast
        for u in await repo.get_all_users():
            try:
                logger.debug(u.update_delay_min)
                logger.debug(u.last_update_time)

                if (datetime.now() - u.last_update_time).seconds / 60 >= u.update_delay_min:
                   u.last_update_time = datetime.now()
                   await repo.save_user(u)

                   await bot.send_message(u.tg_id, answer_text)
                else:
                    logger.debug("Skip user, wait")
            except aiogram.exceptions.AiogramError as e:
                logger.error(f"Error when send broadcast to user {u}: '{e}'")


        # Wait
        await asyncio.sleep(UPDATE_TIME * 60)