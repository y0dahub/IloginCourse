from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

class AiogramPaginator:
    def __init__(self, db, items_per_page: int, chat_id: int):
        self.db = db
        self.items_per_page = items_per_page
        self.chat_id = chat_id
        self.callback_data = CallbackData('page', 'action', 'page')

    def get_pagination_buttons(self, current_page: int, total_pages: int) -> InlineKeyboardMarkup:
        buttons = []

        if current_page > 1:
            buttons.append(InlineKeyboardButton("◀️ Предыдущая", callback_data=self.callback_data.new(action='prev', page=current_page - 1)))
        
        if current_page < total_pages:
            buttons.append(InlineKeyboardButton("Следующая ▶️", callback_data=self.callback_data.new(action='next', page=current_page + 1)))
        
        return InlineKeyboardMarkup(row_width=2).add(*buttons)

    async def get_paginated_courses(self, page: int, interest: str | list[str]):
        total_courses = await self.db.get_total_courses_by_interest(interest)
        total_pages = self.get_max_page(total_courses)

        page = max(1, min(page, total_pages))

        courses = await self.db.get_courses_paginated(page, self.items_per_page, interest)

        return {
            'courses': courses,
            'current_page': page,
            'total_pages': total_pages,
            'total_courses': total_courses
        }

    def get_max_page(self, total_items: int) -> int:
        return (total_items + self.items_per_page - 1) // self.items_per_page

    async def send_courses_page(self, message, page: int, interest: str | list[str]):
        result = await self.get_paginated_courses(page, interest)

        courses = result['courses']
        current_page = result['current_page']
        total_pages = result['total_pages']

        course_message = "\n".join([f"{i+1}. {course['name']} - {course['description']}" for i, course in enumerate(courses)])

        pagination_buttons = self.get_pagination_buttons(current_page, total_pages)

        await message.answer(
            course_message if course_message else "Курсы не найдены.",
            reply_markup=pagination_buttons
        )

    async def process_page(self, callback_query, interest: str | list[str]):
        current_page = int(callback_query.data.split(":")[1])
        action = callback_query.data.split(":")[0]

        if action == 'prev' and current_page > 1:
            new_page = current_page - 1
        elif action == 'next' and current_page < self.get_max_page(await self.db.get_total_courses_by_interest(interest)):
            new_page = current_page + 1
        else:
            return

        await self.send_courses_page(callback_query.message, new_page, interest)

        await callback_query.answer()
