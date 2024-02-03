from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base
from .task import Task


class User(Base):
    telegram_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
    username: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship()
