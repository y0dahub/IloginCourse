from config import CREATE_QUERY_USERS, CREATE_QUERY_COURSES, \
    QUERY_ADD_USERS, QUERY_CHECK_USER_EXISTS, QUERY_CHECK_USER_EXISTS, \
    QUERY_ADD_COURSE, QUERY_DELETE_COURSE, QUERY_CHECK_COURSE_EXISTS, \
    QUERY_ADD_NEW_INTEREST, QUERY_DELETE_INTEREST, QUERY_GET_USER_INTERESTS, \
    QUERY_GET_COURSES_BY_INTEREST_STRING, QUERY_GET_COURSES_BY_INTEREST_LIST, \
    QUERY_GET_COURSE_BY_ID, QUERY_GET_USERS_BY_INTEREST, QUERY_GET_ALL_COURSES_STRING, \
    QUERY_GET_ALL_COURSES_LIST

from paginator.paginator import Paginator

import asyncpg


class Database:
    def __init__(self, user, password, host, database_name):
        self.user = user
        self.password = password
        self.host = host
        self.database_name = database_name

    async def connect(self):
        self.conn = await asyncpg.connect(host=self.host, user=self.user, 
                              password=self.password, database=self.database_name)
        
    async def close(self):
        if self.conn:
            await self.conn.close()

    async def init_database_and_tables(self):
        await self.connect()
        try:
            await self.conn.execute(CREATE_QUERY_USERS)
            await self.conn.execute(CREATE_QUERY_COURSES)
        except Exception as _err:
            raise _err
    
    async def user_exists(self, user_id: int):
        await self.connect()

        try:
            result = await self.conn.fetchval(QUERY_CHECK_USER_EXISTS, user_id)
            return result > 0
        except Exception as _err:
            raise _err

    async def course_exists(self, name: str):
        await self.connect()

        try:
            result = await self.conn.fetchval(QUERY_CHECK_COURSE_EXISTS, name)
            return result > 0
        except Exception as _err:
            raise _err



    async def add_user(self, user_id: int, name: str, interests: list[str]):
        await self.connect()

        try:
            if not await self.user_exists(user_id):
                await self.conn.execute(QUERY_ADD_USERS, user_id, name, interests)
        except Exception as _err:
            raise _err      


    async def add_course(self, name: str, url: str, interest: str, description: str):
        await self.connect()

        try:
            if not await self.course_exists(name=name):
                await self.conn.execute(QUERY_ADD_COURSE, name, url, interest, description)
        except Exception as _err:
            raise _err

    async def delete_course(self, course_id: int):
        await self.connect()

        try:
            await self.conn.execute(QUERY_DELETE_COURSE, course_id)
        except Exception as _err:
            raise _err

    async def get_courses_by_interest(self, interest: str | list[str]):
        await self.connect()

        try:
            if isinstance(interest, str):
                result = await self.conn.fetch(QUERY_GET_COURSES_BY_INTEREST_STRING, interest)
            elif isinstance(interest, list):
                result = await self.conn.fetch(QUERY_GET_COURSES_BY_INTEREST_LIST, interest)
            else:
                raise ValueError("Интерес должен предоставляться в формате string | list")
            
            return result
        
        except Exception as _err:
            raise _err

    async def get_course_by_id(self, course_id: int):
        await self.connect()

        try:
            result = await self.conn.fetch(QUERY_GET_COURSE_BY_ID, course_id)
            return result[0] if result is not None else None
        except Exception as _err:
            raise _err

    async def get_total_courses_by_interest(self, interest: str | list[str]) -> int:
        await self.connect()
        try:
            if isinstance(interest, str):
                result = await self.conn.fetchval(QUERY_GET_ALL_COURSES_STRING, interest)
            elif isinstance(interest, list):
                result = await self.conn.fetchval(QUERY_GET_ALL_COURSES_LIST, interest)
            else:
                raise ValueError("Интерес должен быть строкой или списком строк.")
            
            return result
        except Exception as _err:
            raise _err

    async def get_courses_by_interest_paginated(self, interest: str | list[str], page: int, page_size: int):
        courses = await self.get_courses_by_interest(interest)
        
        paginator = Paginator(courses, page_size)
        paginated_courses = paginator.get_page(page)
        navigation = paginator.get_navigation(page)
        
        return paginated_courses, navigation

    
    async def add_interest(self, user_id: int, new_interest: str):
        await self.connect()

        try:
            await self.conn.execute(QUERY_ADD_NEW_INTEREST, new_interest, user_id)
        except Exception as _err:
            raise _err

    async def delete_interest(self, user_id: int, interest_to_delete: str):
        await self.connect()

        try:
            await self.conn.execute(QUERY_DELETE_INTEREST, interest_to_delete, user_id)
        except Exception as _err:
            raise _err

    async def get_user_interests(self, user_id: int):
        await self.connect()

        try:
            result = await self.conn.fetch(QUERY_GET_USER_INTERESTS, user_id)
            
            if result:
                return result[0]['interests'] if 'interests' in result[0] else []
            return []
        except Exception as _err:
            raise _err

    async def get_users_by_interest(self, interest: int):
        await self.connect()
        
        try:
            result = await self.conn.fetch(QUERY_GET_USERS_BY_INTEREST, interest)
            return result if result else None
        except Exception as _err:
            raise _err
        