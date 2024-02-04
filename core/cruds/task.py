from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

from web_service.api_v1.tasks.schemas import TaskCreate
from core.models.task import Task
from core.models.user import User


async def create_task(
        session: AsyncSession,
        task_in: TaskCreate,
) -> Task:
    task = Task(**task_in.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task(
        session: AsyncSession,
        task_id: int,
) -> Union[Task, None]:
    return await session.get(Task, task_id)


async def get_tasks(session: AsyncSession) -> list[Task]:
    stmt = select(Task).order_by(Task.create_date)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return tasks


async def get_tasks_current_user(
        session: AsyncSession,
        telegram_user_id: int
) -> list[Result]:
    stmt = (
        select(Task.id, Task.description, Task.create_date, User)
        .join(User.tasks)
        .where(User.telegram_id == telegram_user_id)
        .order_by(Task.create_date)
    )
    result: Result = await session.execute(stmt)
    return result


async def delete_task(
        session: AsyncSession,
        task: Task
) -> None:
    await session.delete(task)
    await session.commit()
