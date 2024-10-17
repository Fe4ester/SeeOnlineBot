from aiogram.fsm.state import StatesGroup, State


class CheckStates(StatesGroup):
    set = State()
    delete = State()
    periods = State()
