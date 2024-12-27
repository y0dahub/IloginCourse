from aiogram.filters import CommandStart
from aiogram.filters import or_f
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from keyboards.inline import build_languages_kb
from keyboards.reply import build_admin_menu_kb, build_menu_kb
from constats import DB

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
            f"Приветствую тебя, {message.from_user.first_name}.\n"
            "Для работы бота необходимо ответить на вопрос:\n\n"
            "*Какой язык программирования ты хочешь учить* (на основе ответа будут предложены рекомендации к изучению)",
            reply_markup=languages_kb,
            parse_mode="MARKDOWN"
        )
    else:
        if user_id in LIST_OF_ADMINS:
            await message.answer(
                f"Приветствую тебя, {message.from_user.first_name}.\nВыберите действие:",
                reply_markup=admin_menu_kb
            )
        else:
            await message.answer(
                f"Приветствую тебя, {message.from_user.first_name}.\n",
                reply_markup=menu_kb
            )
