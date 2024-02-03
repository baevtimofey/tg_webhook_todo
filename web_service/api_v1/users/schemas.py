from pydantic import BaseModel


class UserBase(BaseModel):
    telegram_id: int
    username: str


class UserCreate(UserBase):
    pass
