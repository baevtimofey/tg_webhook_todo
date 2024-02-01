from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper
from core.cruds import task as crud_task
from web_service.api_v1.tasks import schemas

bot = Bot(settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    text = """Добро пожаловать в телеграмм бота, который помогает тебе со списком задачь
    
/add  - добавить задачу 
/list - вывести список задач (сортировка по дате добавления). 
    """
    await message.answer(text)


@dp.message(Command("add"))
async def add_task(message: types.Message):
    task_data = {
        "title": "Title todo",
        "description": "More description",
    }
    task = schemas.TaskCreate(**task_data)
    sess = db_helper.get_async_session()
    await crud_task.create_task(session=sess, task_in=task)
    await message.answer(f"Something was happened")


@dp.message(Command("list"))
async def get_tasks(message: types.Message):
    await message.answer("press to list")

# @dp.message()
# async def other_events():
#     pass
