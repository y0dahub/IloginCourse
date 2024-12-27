from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def build_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Просмотреть курсы")],
            [KeyboardButton(text="Редактировать интересы")]
        ],
        resize_keyboard=True
    )

async def build_interests_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить интерес")],
            [KeyboardButton(text="Удалить интерес")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


async def build_admin_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Просмотреть курсы")],
            [KeyboardButton(text="Редактировать интересы")],
            [KeyboardButton(text="Упраление курсами")],
            [KeyboardButton(text="Главное меню")],
        ],
        resize_keyboard=True
    )

async def build_courses_manager_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить курс")],
            [KeyboardButton(text="Удалить курс")],
            [KeyboardButton(text="Редактировать курс")]
        ],
        resize_keyboard=True
    )