from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def start_cmd(msg: types.Message) -> None:
    await msg.answer(f"Hello, {msg.from_user.full_name}!")