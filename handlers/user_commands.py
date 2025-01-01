from aiogram.filters import CommandStart, Command
from aiogram.filters import or_f
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from keyboards.inline import build_languages_kb
from keyboards.reply import build_admin_menu_kb, build_menu_kb
from constats import DB, INTERESTS

from config import LIST_OF_ADMINS

router = Router()
db = DB

@router.message(or_f(CommandStart(), F.text == "Главное меню"))
async def greeting(message: Message, state: FSMContext):
    languages_kb = await build_languages_kb()
    admin_menu_kb = await build_admin_menu_kb()
    menu_kb = await build_menu_kb()

    user_id = int(message.from_user.id)

    if not await db.user_exists(user_id=user_id):
        await state.update_data({"user_id": user_id, "name": message.from_user.first_name})

        await message.answer(
            f"Приветствую тебя, {message.from_user.first_name}! 🎉👋\n\n"
            "Перед тем как мы начнем, ответь на один важный вопрос: 🧐\n\n"
            "*Что ты хочешь изучать в сфере IT?* 💻✨\n\n"
            "На основе твоего выбора я предложу рекомендации, чтобы ты мог начать обучение с удовольствием! 🚀📚",
            reply_markup=languages_kb,
            parse_mode="MARKDOWN"
        )
    else:
        if user_id in LIST_OF_ADMINS:
            await message.answer(
                f"Приветствую тебя, {message.from_user.first_name}! 🎉👋",
                reply_markup=admin_menu_kb
            )
        else:
            await message.answer(
                f"Приветствую тебя, {message.from_user.first_name}! 🎉👋",
                reply_markup=menu_kb
            )


@router.message(Command("find"))
async def find(message: Message):
    try:
        interest = message.text.split(" ")[1]
        page = 1
        page_size = 1

        if interest in INTERESTS:
            courses, navigation = await db.get_courses_by_interest_paginated(interest=interest, page=page, page_size=page_size)

            if courses:
                message_text = f"Курсы по вашему интересу '{interest}':\n"
                for course in courses:
                    message_text += f"📚 *{course['name']}*\n[Перейти]({course['url']})\n\n"

                buttons = []
                if navigation.get('has_previous'):
                    buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"find_page:{interest}:{navigation['previous_page']}"))
                if navigation.get('has_next'):
                    buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"find_page:{interest}:{navigation['next_page']}"))

                keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

                await message.answer(message_text, reply_markup=keyboard, parse_mode="MARKDOWN")
            else:
                await message.answer(f"Курсы по интересу '{interest}' не найдены.")
        else:
            await message.answer(f"Интерес '{interest}' не найден.")

    except Exception as e:
        print(f"Ошибка: {e}")
        await message.answer("Произошла ошибка при поиске курсов.")


@router.callback_query(lambda c: c.data.startswith("find_page:"))
async def handle_find_pagination(callback_query: CallbackQuery):
    try:
        _, interest, page = callback_query.data.split(":")
        page = int(page)
        page_size = 1

        courses, navigation = await db.get_courses_by_interest_paginated(interest=interest, page=page, page_size=page_size)

        if courses:
            message_text = f"Курсы по вашему интересу '{interest}':\n"
            for course in courses:
                message_text += f"📚 *{course['name']}*\n[Перейти]({course['url']})\n\n"

            buttons = []
            if navigation.get('has_previous'):
                buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"find_page:{interest}:{navigation['previous_page']}"))
            if navigation.get('has_next'):
                buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"find_page:{interest}:{navigation['next_page']}"))

            keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

            await callback_query.message.edit_text(message_text, reply_markup=keyboard, parse_mode="MARKDOWN")
        else:
            await callback_query.answer("Курсы не найдены по вашему интересу.")

    except Exception as e:
        print(f"Ошибка: {e}")
        await callback_query.answer("Произошла ошибка при обработке пагинации.")
