import asyncio, sqlite3
from SQLite.sql_start import execute_query, execute_read_query

async def insert_file(name, description, date, user_id, media_type, connection):
    input_file = f"""
    INSERT INTO 
      media (name, description, date, user_id, media_type)
    VALUES
      ('{name.lower()}', '{description}', '{date}', {user_id}, '{media_type}')
    """
    await execute_query(connection, input_file)

async def select_files(connection, name, date, user_id, media_type):
    select_name = f"""
        SELECT id, name, description, date, user_id, media_type
        FROM media
        WHERE name = '{name.lower()}' AND date = '{date}' AND user_id = {user_id} AND media_type = '{media_type}'
        """
    return execute_read_query(connection, select_name)

async def select_file_id(connection, name, description, date, user_id, media_type):
    select_id = f"""
        SELECT id, name, description, date, user_id, media_type
        FROM media
        WHERE name = '{name.lower()}' AND description = '{description}' AND date = '{date}' AND user_id = {user_id} AND media_type = '{media_type}' 
        """
    return execute_read_query(connection, select_id)

async def select_file_where(connection, where):
    file_where = f"""
        SELECT id, name, description, date, user_id, media_type
        FROM media
        WHERE {where} 
        """
    return execute_read_query(connection, file_where)

async def update_file_description(connection, media_id, description):
    update_file = f"""
    UPDATE media
    SET description = "{description}"
    WHERE id = {media_id}    
    """
    return await execute_query(connection, update_file)

async def delete_file_media(connection, media_id):
    delete_id = f"""
            DELETE FROM media
            WHERE id = {media_id} 
            """
    await execute_query(connection, delete_id)
