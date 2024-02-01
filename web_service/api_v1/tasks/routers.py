from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import Task, TaskCreate
from core.models import db_helper
from core.cruds import task as task_crud

router = APIRouter(tags=["Tasks"])


@router.get(
    path="/",
    response_model=list[Task]
)
async def get_tasks(session: AsyncSession = Depends(db_helper.get_async_session)):
    return await task_crud.get_tasks(session=session)


@router.post(
    path="/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED
)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(db_helper.get_async_session),
):
    return await task_crud.create_task(session=session, task_in=task_in)


@router.delete(path="/{task_id}")
async def delete_task(
    task: Task = Depends(),
    session: AsyncSession = Depends(db_helper.get_async_session),
):
    return await task_crud.delete_task(session=session, task=task)
