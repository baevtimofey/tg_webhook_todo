from datetime import datetime

from sqlalchemy import Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Task(Base):
    description: Mapped[str] = mapped_column(Text())
    create_date: Mapped[datetime] = mapped_column(default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
