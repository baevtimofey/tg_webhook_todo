from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, requests
from aiogram import types, Dispatcher, Bot

from bot.telegram_bot import bot, dp
from core.config import settings
from api_v1 import router as api_v1_router


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
    lifespan=lifespan,
)
app.include_router(router=api_v1_router, prefix=settings.API_V1_PREFIX)


@app.post(settings.WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    if telegram_update.message.entities:
        print(f"Started {telegram_update.message.text}")
    else:
        print(f"Simple text --> {telegram_update.message.text}")
    await dp.feed_update(bot, telegram_update)


if __name__ == '__main__':
    uvicorn.run(
        app="web_server:app",
        reload=True,
        port=8080
    )
