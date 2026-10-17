from aiogram.fsm.state import State, StatesGroup

class Booking(StatesGroup):
    waiting_for_date = State()
    waiting_for_comment = State()
    waiting_for_confirm = State()