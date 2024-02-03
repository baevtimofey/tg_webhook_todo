from typing import Union

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User
from web_service.api_v1.users.schemas import UserCreate


async def create_user(
    session: AsyncSession,
    user_in: UserCreate,
) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(
    session: AsyncSession,
    user_id: int,
) -> Union[User, None]:
    return await session.get(User, user_id)


async def get_user_by_telegram_id(
    session: AsyncSession,
    user_telegram_id: int,
) -> Union[User, None]:
    stmt = select(User).where(User.telegram_id == user_telegram_id)
    result: Result = await session.scalars(statement=stmt)
    user = result.all()
    if len(user) == 0:
        return None
    return user
