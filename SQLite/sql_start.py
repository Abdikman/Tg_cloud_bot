import sqlite3, asyncio
from sqlite3 import Error

create_table_media = """
CREATE TABLE IF NOT EXISTS media (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  date TEXT NOT NULL,
  user_id INTEGER,
  media_type TEXT NOT NULL
);
"""

"""Функция создаёт БД и таблицу или сразу подключается к ней"""
async def create_connection(check):
    connection = None
    try:
        connection = sqlite3.connect("SQlite/bd.sqlite")
        print("Подключение к БД... 'SQlite/bd.sqlite'")

        if check:
            await execute_query(connection, create_table_media)

        return connection
    except Error as e:
        print(f"Произошла ошибка создания БД: '{e}'")


"""Функция выполнения запросов"""
async def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Запрос выполнен")
    except Error as e:
        print(f"Произошла ошибка в запросе: '{e}'")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Ошибка: '{e}'")
