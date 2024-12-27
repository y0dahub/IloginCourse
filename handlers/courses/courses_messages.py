from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from forms.course_form import CourseInfo, CourseDeleteInfo
from paginator.paginator import AiogramPaginator

from keyboards.reply import build_courses_manager_menu, build_menu_kb, build_admin_menu_kb
from constats import DB, BOT

from config import LIST_OF_ADMINS

router = Router()
db = DB
bot = BOT

@router.message(F.text == "Просмотреть курсы")
async def send_courses_with_interest(message: Message):
    user_id = message.from_user.id

    admin_kb = await build_admin_menu_kb()
    menu_kb = await build_menu_kb()
    
    current_interests = await db.get_user_interests(user_id=user_id)
    current_courses = await db.get_courses_by_interest(interest=current_interests)

    print(current_courses)

    if current_courses:
        courses_text = "\n\n".join([f"'*{course['name']}*'\n*{course['description']}*\n[Ссылка на курс]({course['url']})\n\n(id = {course['id']})" 
                                   for course in current_courses])
    else:
        courses_text = "Курсы по вашему запросу не найдены."
    
    await message.answer(
        courses_text, 
        parse_mode="MARKDOWN", 
        reply_markup=admin_kb if user_id in LIST_OF_ADMINS else menu_kb
    )



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
    url = message.text

    if url.startswith("http://"):
        await message.answer("Некорректный URL.\n URL должен начинаться с httpS")
        return

    await state.update_data({"url": url})
    await message.answer("Теперь введи описание курса.")
    await state.set_state(CourseInfo.description)

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

    if not is_course_exists:
        await db.add_course(name=name, interest=interest, url=url, description=description)
        await message.answer(f"Успех!\nКурс '{name}' добавлен!\n\n")

        for user in users_in_interest:
            user_id = user['id']
            await bot.send_message(user_id, f"Новый курс по интересу '{interest}':\n*{name}\n{description}\n[Ссылка на курс]({url})",
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



