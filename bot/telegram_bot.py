from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart

from core.config import settings

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
    await message.answer("press to add")


@dp.message(Command("list"))
async def get_tasks(message: types.Message):
    await message.answer("press to list")

# @dp.message()
# async def other_events():
#     pass
