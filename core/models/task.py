from datetime import datetime

from sqlalchemy import Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Task(Base):
    title: Mapped[str]
    description: Mapped[str] = mapped_column(Text())
    create_date: Mapped[datetime]
