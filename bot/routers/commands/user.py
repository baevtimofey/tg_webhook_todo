from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.states.form_task import FormTask
from core.cruds.user import get_user_by_telegram_id
from core.cruds.task import create_task, get_tasks_current_user, delete_task, get_task
from core.models import db_helper
from web_service.api_v1.tasks import schemas

router = Router()


async def is_task_exceeded(
        message: types.Message,
        limit: int = 5,
) -> bool:
    async with db_helper.session_factory() as sess:
        tasks = await get_tasks_current_user(
            session=sess,
            telegram_user_id=message.from_user.id
        )
        return len(tasks) < limit


@router.message(Command("add"))
async def add_task(
        message: types.Message,
        state: FSMContext,
) -> None:
    if await is_task_exceeded(message):
        await state.set_state(FormTask.description)
        await message.answer(f"Какую задачу нужно поместить в todo?")
    else:
        await message.answer("Максимальное количество задач = 5")


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
    await message.delete()
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
    await message.delete()
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


class ListTaskCallback(CallbackData, prefix="task"):
    action: str
    task_id: int
    message_id: int


async def build(message: types.Message):
    builder = InlineKeyboardBuilder()
    session = await db_helper.get_async_session()
    tasks = await get_tasks_current_user(
        session=session,
        telegram_user_id=message.from_user.id
    )
    for task in tasks:
        builder.button(
            text=f"{task.description} {task.create_date.strftime('%d %b - %H:%M')}",
            callback_data=ListTaskCallback(action="delete", task_id=task.id, message_id=message.message_id)
        )
    builder.adjust(1)

    return builder


@router.message(Command("list"))
async def show_tasks(message: types.Message):
    text = "Задачи"
    builder = await build(message)
    await message.answer(
        text=text,
        reply_markup=builder.as_markup()
    )
    print(f"message_id of /list{message.message_id}")


@router.callback_query(ListTaskCallback.filter(F.action == "delete"))
async def del_task(
        query: CallbackQuery,
        callback_data: ListTaskCallback,
):
    async with db_helper.session_factory() as sess:
        task = await get_task(
            session=sess,
            task_id=callback_data.task_id
        )
        await delete_task(
            session=sess,
            task=task
        )
    await query.message.answer("Задача удалена.\nНажмите /list")
