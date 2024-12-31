from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

async def build_languages_kb():
    languages_kb = InlineKeyboardBuilder()
    

    languages_kb.row(
        InlineKeyboardButton(text="Python: 🐍✨", callback_data="lang_python"),
        InlineKeyboardButton(text="C++: 💻🔧", callback_data="lang_cpp"),
        InlineKeyboardButton(text="Kotlin: ☕️📱", callback_data="lang_java"),
        InlineKeyboardButton(text="Java: ☕️🌍", callback_data="lang_go"),
        InlineKeyboardButton(text="Go: 🐹🚀", callback_data="lang_kotlin"),
        width=2
    )

    return languages_kb.as_markup()


async def build_current_interests_kb(interests: list[str], current_interests: list[str] | str, mode: str = "add"):
    interests_kb = InlineKeyboardBuilder()
    new_interests = []

    if isinstance(current_interests, str):
        current_interests = [current_interests]

    if mode == "delete":
        for interest in current_interests:
            interests_kb.row(
                InlineKeyboardButton(text=interest.capitalize(), callback_data=f"{mode}_interest_{interest.lower()}"),
                width=2
            )
        return interests_kb.as_markup()

    for interest in interests:
        if interest not in current_interests:
            new_interests.append(interest)

    if not new_interests:
        return interests_kb.as_markup()
    
    for interest in new_interests:
        interests_kb.row(
            InlineKeyboardButton(text=interest.capitalize(), callback_data=f"{mode}_interest_{interest.lower()}"),
            width=2
        )

    return interests_kb.as_markup()
