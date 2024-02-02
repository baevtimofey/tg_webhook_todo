from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    text = """Добро пожаловать в телеграмм бота, который помогает тебе со списком задачь

/add  - добавить задачу 
/list - вывести список задач (сортировка по дате добавления). 
    """
    await message.answer(text)
