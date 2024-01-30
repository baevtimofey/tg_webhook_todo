from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot

from bot.telegram_bot import bot, dp
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != settings.WEBHOOK_URL:
        await bot.set_webhook(
            url=settings.WEBHOOK_URL
        )

    yield

    await bot.session.close()


app = FastAPI(
    lifespan=lifespan
)


@app.post(settings.WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot, telegram_update)


if __name__ == '__main__':
    uvicorn.run(
        app="web_server:app",
        reload=True,
        port=8080
    )
