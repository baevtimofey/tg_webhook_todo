from aiogram import types, Router
from aiogram.filters import Command

from core.models import db_helper
from core.cruds import task as task_crud
from web_service.api_v1.tasks import schemas

router = Router()


@router.message(Command("add"))
async def add_task(message: types.Message):
    task_data = {
        "description": "More description",
        "user_id": 1
    }
    task = schemas.TaskCreate(**task_data)
    sess = db_helper.get_async_session()
    sess = await anext(sess)
    await task_crud.create_task(session=sess, task_in=task)
    await message.answer(f"Something was happened")


@router.message(Command("list"))
async def get_tasks(message: types.Message):
    await message.answer("press to list")
