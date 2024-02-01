from fastapi import APIRouter

from .tasks.routers import router as tasks_router

router = APIRouter()
router.include_router(router=tasks_router, prefix="/tasks")
