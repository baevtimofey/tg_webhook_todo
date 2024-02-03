from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.states.form_task import FormTask
from core.cruds.user import get_user_by_telegram_id
from core.cruds.task import create_task
from core.models import db_helper
from web_service.api_v1.tasks import schemas

router = Router()


@router.message(Command("add"))
async def add_task(
        message: types.Message,
        state: FSMContext,
) -> None:
    await state.set_state(FormTask.description)
    await message.answer(f"Какую задачу нужно поместить в todo?")


@router.message(FormTask.description)
async def process_description(
        message: types.Message,
        state: FSMContext,
) -> None:
    await state.update_data(description=message.text)
    await state.set_state(FormTask.confirm)
    await message.answer(
        f"Добавить задачу {message.text} в Ваш todo?",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text="Да"),
                    types.KeyboardButton(text="Нет"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@router.message(
    FormTask.confirm,
    lambda mess: mess.text == "Нет",
)
async def process_dont_confirm(
        message: types.Message,
        state: FSMContext,
) -> None:
    await state.clear()
    await message.answer(
        "Отмена записи задачи в todo.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(
    FormTask.confirm,
    lambda mess: mess.text == "Да",
)
async def process_confirm(
        message: types.Message,
        state: FSMContext,
) -> None:
    session = await db_helper.get_async_session()
    user_telegram_id = message.from_user.id
    user = await get_user_by_telegram_id(
        session=session,
        user_telegram_id=user_telegram_id
    )
    data = await state.update_data(user_id=user.id)
    await state.clear()
    task_in = schemas.TaskCreate(**data)
    await create_task(
        session=session,
        task_in=task_in
    )
    await message.answer(
        "Задание добавленно в todo.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(FormTask.confirm)
async def process_unknown_write_bots(message: types.Message) -> None:
    await message.reply("Ожидаю подтверждение.")


@router.message(Command("list"))
async def get_tasks(message: types.Message):
    await message.answer("press to list")
