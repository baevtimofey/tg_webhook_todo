from aiogram import Router

from .commands import router as commands_router
from .common import router as common_router

router = Router()
router.include_router(commands_router)
router.include_router(common_router)
