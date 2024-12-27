from aiogram import F, Router
from aiogram.types import Message

from keyboards.reply import build_interests_kb
from keyboards.inline import build_current_interests_kb
from constats import DB, INTERESTS

db = DB
router = Router()

@router.message(F.text == "Редактировать интересы")
async def edit_menu_interests(message: Message):
    menu_actions_for_interests = await build_interests_kb()
    current_interests = await db.get_user_interests(user_id=int(message.from_user.id))

    interests_text = ", ".join(current_interests) if current_interests else "Нет интересов"

    await message.answer(
        f"*Выбирай нужное действие*\n\nТвои интересы: *{interests_text}*",
        reply_markup=menu_actions_for_interests,
        parse_mode="MARKDOWN"
    )


@router.message(F.text == "Добавить интерес")
async def add_interest_(message: Message):
    current_interests = await db.get_user_interests(user_id=int(message.from_user.id))

    langs = await build_current_interests_kb(interests=INTERESTS, current_interests=current_interests)

    await message.answer("Отлично. Добавить, так добавить...\n\n*Выбери нужный*",
                         reply_markup=langs,
                         parse_mode="MARKDOWN")
    

@router.message(F.text == "Удалить интерес")
async def delete_interest_(message: Message):
    current_interests = await db.get_user_interests(user_id=int(message.from_user.id))
    
    langs = await build_current_interests_kb(interests=INTERESTS, current_interests=current_interests, mode="delete")

    await message.answer("Отлично. Удалить, так удалить...\n\n*Выбери нужный*",
                         reply_markup=langs,
                         parse_mode="MARKDOWN")