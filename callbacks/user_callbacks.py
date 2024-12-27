from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F


from keyboards.reply import build_menu_kb
from constats import DB

router = Router()
db = DB


@router.callback_query(F.data.startswith("lang_"))
async def get_interesting_lang(callback: CallbackQuery, state: FSMContext):
    selected_language = callback.data.split("_")[1]
    menu_kb = await build_menu_kb()

    await callback.message.delete()
    await state.update_data({"interests": [selected_language]})

    data = await state.get_data()
    user_id = data.get("user_id")
    name = data.get("name")
    interests = data.get("interests")


    await db.add_user(user_id=user_id, name=name, interests=interests)
    await callback.answer(f"Ты выбрал язык: {selected_language.capitalize()}.")
    await callback.message.answer("Спасибо! Теперь мы можем продолжить.",
                                  reply_markup=menu_kb)
    

@router.callback_query(F.data.startswith("add_interest_"))
async def add_interest(callback: CallbackQuery):
    await callback.message.delete()
    menu_kb = await build_menu_kb()

    interest = callback.data.split("_")[2]
    user_id = int(callback.from_user.id)

    await db.add_interest(user_id=user_id, new_interest=interest)

    await callback.message.answer("Интерес добавлен!", reply_markup=menu_kb)


@router.callback_query(F.data.startswith("delete_interest_"))
async def add_interest(callback: CallbackQuery):
    await callback.message.delete()
    menu_kb = await build_menu_kb()

    interest = callback.data.split("_")[2]
    user_id = int(callback.from_user.id)

    await db.delete_interest(user_id=user_id, interest_to_delete=interest)

    await callback.message.answer("Интерес удален!", reply_markup=menu_kb)
