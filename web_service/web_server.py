from contextlib import asynccontextmanager

from fastapi import FastAPI

from bot.telegram_bot import bot
from core.config import settings
from web_service.api_v1 import router as api_v1_router
from web_service.webhook.telegram_router import router as telegram_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != settings.WEBHOOK_URL:
        await bot.set_webhook(
            url=settings.WEBHOOK_URL
        )

    yield

    await bot.session.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router=api_v1_router, prefix=settings.API_V1_PREFIX)
app.include_router(router=telegram_router)
