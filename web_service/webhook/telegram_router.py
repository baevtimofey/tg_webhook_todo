from fastapi import APIRouter
from aiogram import types

from core.config import settings
from bot.telegram_bot import bot, dp

router = APIRouter(tags=["Webhooks"])


@router.post(settings.WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot, telegram_update)
