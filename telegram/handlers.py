from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from soupsieve import match

from models import ServiceStatus
from parser.abstract_parser import AbstractDownDetectorParser
from repo.abstract_repo import AbstractRepo

router = Router()

@router.message(CommandStart())
async def start_cmd(msg: types.Message, repo: AbstractRepo) -> None:
    repo.save_user(str(msg.from_user.id))
    await msg.answer(f"Hello, {msg.from_user.full_name}!")


@router.message(Command("users"))
async def users_cmd(msg: types.Message, repo: AbstractRepo) -> None:
    all_users = repo.get_all_users()

    answer_text = " ".join(all_users)
    if not answer_text:
        return

    await msg.answer(answer_text)

@router.message(Command("stats"))
async def stats_cmd(msg: types.Message, parser: AbstractDownDetectorParser) -> None:
    services = parser.get_problems_services()

    answer_text = ""

    status_smail = ""
    for s in services:
        match s.problem_status:
            case ServiceStatus.OK:
                status_smail = "🟢"
            case ServiceStatus.WARNING:
                status_smail = "🟡"
            case ServiceStatus.ERROR:
                status_smail = "🔴"

        answer_text += f"{status_smail} {s.service_name}\n"

    await msg.answer(answer_text)