from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

from web_service.api_v1.tasks.schemas import TaskCreate
from core.models.task import Task


async def create_task(
    session: AsyncSession,
    task_in: TaskCreate,
) -> Task:
    task = Task(**task_in.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_tasks(session: AsyncSession) -> list[Task]:
    stmt = select(Task).order_by(Task.create_date)
    result: Result = await session.execute(stmt)
    cards = result.scalars().all()
    return cards


async def delete_task(
    session: AsyncSession,
    task: Task
) -> None:
    await session.delete(task)
    await session.commit()
