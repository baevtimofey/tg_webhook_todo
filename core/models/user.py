from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .task import Task


class User(Base):
    telegram_id: Mapped[int]
    username: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship()
