from aiogram import types, Router
from aiogram.filters import Command

router = Router()


@router.message(Command("add"))
async def add_task(message: types.Message):
    await message.answer(f"Something was happened")


@router.message(Command("list"))
async def get_tasks(message: types.Message):
    await message.answer("press to list")
