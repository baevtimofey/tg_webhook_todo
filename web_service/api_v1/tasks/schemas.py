from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    description: str
    user_id: int


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
