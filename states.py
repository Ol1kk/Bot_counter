from aiogram.fsm.state import StatesGroup
from aiogram.fsm.state import State

class Income(StatesGroup):
    waiting_for_income = State()