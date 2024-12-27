from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

TOKEN = getenv("TOKEN")
DB_DATA = {
    "user": getenv("DB_USER"),
    "password": getenv("DB_PASSWORD"),
    "host": getenv("DB_HOST"),
    "database_name": getenv("DB_NAME")
}

LIST_OF_ADMINS = [7138248711]


CREATE_QUERY_USERS = """
            CREATE TABLE IF NOT EXISTS users (
                id BIGINT NOT NULL,
                name VARCHAR(50) NOT NULL,
                interests TEXT[]
            )
            """

CREATE_QUERY_COURSES = """
            CREATE TABLE IF NOT EXISTS courses(
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                interest TEXT,
                url TEXT NOT NULL CHECK (url ~ '^(https)://.*$'),
                description TEXT
            )"""

QUERY_ADD_USERS = """
            INSERT INTO users (id, name, interests) 
            VALUES ($1, $2, $3);
            """

QUERY_CHECK_USER_EXISTS = """
            SELECT COUNT(*) 
            FROM users 
            WHERE id = $1;
            """

QUERY_CHECK_COURSE_EXISTS = """
            SELECT COUNT(*)
            FROM courses 
            WHERE name = $1;
            """

QUERY_ADD_COURSE = """
            INSERT INTO courses (name, url, interest, description) 
            VALUES ($1, $2, $3, $4);
            """

QUERY_DELETE_COURSE = """
            DELETE FROM courses 
            WHERE id = $1;
            """

QUERY_ADD_NEW_INTEREST = """
            UPDATE users
            SET interests = array_append(interests, $1)
            WHERE id = $2;
            """

QUERY_DELETE_INTEREST = """
            UPDATE users
            SET interests = array_remove(interests, $1)
            WHERE id = $2;
            """

QUERY_GET_USER_INTERESTS = """
            SELECT interests FROM users
            WHERE id = $1
            """

QUERY_GET_COURSES_BY_INTEREST_STRING = """SELECT * FROM courses WHERE interest = $1"""
QUERY_GET_COURSES_BY_INTEREST_LIST = """SELECT * FROM courses WHERE interest = ANY($1)"""

QUERY_GET_COURSE_BY_ID = """SELECT name FROM courses WHERE id = $1"""
QUERY_GET_USERS_BY_INTEREST = """SELECT id FROM users WHERE interests @> ARRAY[$1]::TEXT[]"""

QUERY_GET_ALL_COURSES_STRING = """SELECT COUNT(*) FROM courses WHERE interest = $1"""
QUERY_GET_ALL_COURSES_LIST = """SELECT COUNT(*) FROM courses WHERE interest = ANY($1)"""

