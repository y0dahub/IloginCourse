from aiogram.fsm.state import State, StatesGroup

class UserInfo(StatesGroup):
    user_id = State()
    name = State()
    interests = State()