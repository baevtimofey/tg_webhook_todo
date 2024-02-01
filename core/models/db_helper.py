from typing import AsyncGenerator
from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, async_scoped_session

from core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            # expire_on_commit=False
        )

    async def get_async_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session

    async def get_async_scope_session(self):
        session: AsyncSession = await async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        yield session
        await session.close()


db_helper = DatabaseHelper(
    url=settings.DB_URL,
    echo=settings.DB_ECHO
)
