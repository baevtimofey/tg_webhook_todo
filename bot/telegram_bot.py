from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

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
