from typing import Union

from aiogram import types
from core.models import db_helper, User
from core.cruds.user import get_user_by_telegram_id, create_user
from web_service.api_v1.users import schemas


async def register_user(message: types.Message) -> None:
    user_telegram_id = message.from_user.id
    username = message.from_user.username
    if await has_user(user_telegram_id) is None:
        sess = await db_helper.get_async_session()
        user_in = schemas.UserCreate(telegram_id=user_telegram_id, username=username)
        await create_user(session=sess, user_in=user_in)


async def has_user(user_telegram_id: int) -> Union[User, None]:
    sess = await db_helper.get_async_session()
    user = await get_user_by_telegram_id(session=sess, user_telegram_id=user_telegram_id)
    return user
