from aiogram import F, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext

from forms.course_form import CourseInfo, CourseDeleteInfo

from keyboards.reply import build_courses_manager_menu, build_menu_kb
from constats import DB, BOT

import re

router = Router()
db = DB
bot = BOT

@router.message(F.text == "Просмотреть курсы")
async def view_courses(message: Message):
    user_id = int(message.from_user.id)
    interest = await db.get_user_interests(user_id=user_id)
    page = 1
    page_size = 1


    try:
        courses, navigation = await db.get_courses_by_interest_paginated(interest, page, page_size)

        if courses:
            message_text = "Курсы по вашему интересу:\n"
            for course in courses:
                message_text += f"📚 *{course['name']}*\n[Перейти]({course['url']})\n\n"

            buttons = []
            if navigation.get('has_previous'):
                buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"page:{navigation['previous_page']}"))

            if navigation.get('has_next'):
                buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"page:{navigation['next_page']}"))

            keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

            await message.answer(message_text, reply_markup=keyboard, parse_mode="MARKDOWN")
        else:
            await message.answer("Курсы не найдены по вашему интересу.")

    except Exception as e:
        raise e


@router.callback_query(lambda c: c.data.startswith("page:"))
async def handle_pagination(callback_query: CallbackQuery):
    page = int(callback_query.data.split(":")[1])
    user_id = int(callback_query.from_user.id)
    interest = await db.get_user_interests(user_id=user_id)
    page_size = 1

    try:
        courses, navigation = await db.get_courses_by_interest_paginated(interest=interest, page=page, page_size=page_size)
        
        if courses:
            message_text = "Курсы по вашему интересу:\n"
            for course in courses:
                message_text += f"📚 *{course['name']}*\n*{course['description']}*\n\n[Перейти]({course['url']})\n\n"
            
            buttons = []
            if navigation['has_previous']:
                buttons.append(
                    InlineKeyboardButton(text="⬅️", callback_data=f"page:{navigation['previous_page']}")
                )
            if navigation['has_next']:
                buttons.append(
                    InlineKeyboardButton(text="➡️", callback_data=f"page:{navigation['next_page']}")
                )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

            await callback_query.message.edit_text(message_text, reply_markup=keyboard, parse_mode="Markdown")
        else:
            await callback_query.answer("Курсы не найдены по вашему интересу.")
    except Exception as e:
        await callback_query.answer("Произошла ошибка при получении курсов.")
        print(f"Ошибка: {e}")



@router.message(F.text == "Упраление курсами")
async def courses_manager(message: Message):
    courses_manager = await build_courses_manager_menu()

    await message.answer("Меню управления курсами:",
                        reply_markup=courses_manager)
    


@router.message(F.text == "Добавить курс")
async def course_add(message: Message, state: FSMContext):
    await message.answer("Введи навзвание курса.")
    await state.set_state(CourseInfo.name)

@router.message(CourseInfo.name)
async def process_course_name(message: Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await message.answer("Теперь введи категорию курса (интерес)")
    await state.set_state(CourseInfo.interest)

@router.message(CourseInfo.interest)
async def process_course_interest(message: Message, state: FSMContext):
    await state.update_data({"interest": message.text})
    await message.answer("Теперь введи URL")
    await state.set_state(CourseInfo.url)

@router.message(CourseInfo.url)
async def process_course_url(message: Message, state: FSMContext):
    url = message.text.strip()

    url_pattern = re.compile(
        r"^https://[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})?(?:/.*)?$"
    )

    if url_pattern.match(url):
        await state.update_data({"url": url})
        await message.answer("Теперь введи описание курса.")
        await state.set_state(CourseInfo.description)
    else:
        await message.answer(
            "Некорректный URL.\n"
            "Пожалуйста, убедитесь, что ваш URL начинается с https:// и является корректным веб-адресом."
        )

@router.message(CourseInfo.description)
async def process_add_course(message: Message, state: FSMContext):
    await state.update_data({"description": message.text})

    data = await state.get_data()

    name = data.get("name")
    interest = data.get("interest")
    url = data.get("url")
    description = data.get("description")

    is_course_exists = await db.course_exists(name=name)

    users_in_interest = await db.get_users_by_interest(interest=interest)

    menu_kb = await build_menu_kb()

    if not is_course_exists:
        await db.add_course(name=name, interest=interest, url=url, description=description)
        await message.answer(f"Успех!\nКурс '{name}' добавлен!\n\n",
                             reply_markup=menu_kb)

        for user in users_in_interest:
            user_id = user['id']
            await bot.send_message(user_id, 
                                   f"Новый курс по интересу `{interest}`: *{name}*\n\n[Перейти]({url})",
                                   parse_mode="MARKDOWN")

    else:
        await message.answer("Неудача!\nКурс с таким названием уже существует")
    
    data.clear()



@router.message(F.text == "Удалить курс")
async def course_delete(message: Message, state: FSMContext):
    await message.answer("Введи ID курса для удаления")
    await state.set_state(CourseDeleteInfo.course_id)

@router.message(CourseDeleteInfo.course_id)
async def process_delete_course(message: Message, state: FSMContext):
    await state.update_data({"id": int(message.text)})

    data = await state.get_data()
    
    course_id = data.get("id")
    record_ = await db.get_course_by_id(course_id=course_id)

    name = record_["name"]
    is_course_exists = await db.course_exists(name=name)


    if is_course_exists:
        await db.delete_course(course_id=course_id)
        await message.answer(f"Успех!\nКурс '{name} (id = {course_id})' удален.\n\n")
    else:
        await message.answer(f"Неудача!\nКурс '{name} (id = {course_id})' был удален ранее или не существует.\n\n")



