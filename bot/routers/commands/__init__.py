from aiogram import Router

from .base import router as base_router
from .user import router as user_router

router = Router()
router.include_router(base_router)
router.include_router(user_router)
