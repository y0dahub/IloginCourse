from aiogram.fsm.state import State, StatesGroup

class CourseInfo(StatesGroup):
    name = State()
    interest = State()
    url = State()
    description = State()

class CourseDeleteInfo(StatesGroup):
    course_id = State()