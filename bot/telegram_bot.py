from aiogram import Bot, Dispatcher

from core.config import settings
from .routers import router as main_router

bot = Bot(settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
dp.include_router(main_router)
