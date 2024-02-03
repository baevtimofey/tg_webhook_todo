from aiogram.fsm.state import State, StatesGroup


class FormTask(StatesGroup):
    description = State()
    confirm = State()
