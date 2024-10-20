from os import wait3

from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from soupsieve import match

from schemas import ServiceStatus, User
from parser.abstract_parser import AbstractDownDetectorParser
from repo.abstract_repo import AbstractRepo

router = Router()

@router.message(CommandStart())
async def start_cmd(msg: types.Message, repo: AbstractRepo) -> None:
    await repo.save_user(User(tg_id=str(msg.from_user.id)))
    await msg.answer(f"Привет, {msg.from_user.full_name}!\n/stats - Все сервисы\n/set_delay [минуты] - указать переодичность отправки отчета")

@router.message(Command("set_delay"))
async def set_delay_cmd(msg: types.Message, repo: AbstractRepo) -> None:
    cmd = msg.text.split(" ")
    if len(cmd) !=  2:
        await msg.answer("Неправильная команда!")
        return
    try:
        delay = int(cmd[1])
    except:
        await msg.answer("Укажите число!")
        return

    if delay < 10:
        await msg.answer("Укажите число больше 10!")
        return
    if delay > 100000:
        await msg.answer("Слишком большое число!")
        return

    users = await repo.get_all_users()

    for u in users:
        if u.tg_id == str(msg.from_user.id):
            u.update_delay_min = delay

            await repo.save_user(u)
            await msg.answer("Успешная измена 😈")
            return
    await msg.answer("Вы не зарегистрированы, введите /start")

@router.message(Command("users"))
async def users_cmd(msg: types.Message, repo: AbstractRepo) -> None:
    all_users = await repo.get_all_users()

    answer_text = "Пользователи: \n"
    for u in all_users:
        answer_text +=f"ID: {u.tg_id}\nUPDATE_DELAY: {u.update_delay_min}\nLAST_UPDATE: {u.last_update_time}\n"

    if not answer_text:
        await msg.answer("Пользователей не найдено!")
        return

    await msg.answer(answer_text)

@router.message(Command("stats"))
async def stats_cmd(msg: types.Message, parser: AbstractDownDetectorParser) -> None:
    services = parser.get_problems_services()

    answer_text = ""

    status_smail = ""
    for s in services:
        match s.service_status:
            case ServiceStatus.OK:
                status_smail = "🟢"
            case ServiceStatus.WARNING:
                status_smail = "🟡"
            case ServiceStatus.ERROR:
                status_smail = "🔴"

        answer_text += f"{status_smail} {s.service_name}\n"

    await msg.answer(answer_text)