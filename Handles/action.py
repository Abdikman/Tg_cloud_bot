from Handles.sql_command import delete_file_media, select_file_where
from Logging_bot.logging_history import history_update
import os
from aiogram import types

from SQLite.sql_start import execute_query


async def rename_file(connection, name, new_name, user_id, media_id, file_type):
    await history_update(user_id,
                         f"\n Пользователь переименовал файл из {name}.{file_type} в {new_name}.{file_type}. Путь:'{media_id}.{file_type}'")
    update_media_name = f"""
    UPDATE media
    SET name = '{new_name}'
    WHERE id = {media_id}
    """
    await execute_query(connection, update_media_name)

async def file_to_user(message, name, user_id, media_id, file_type):
    await history_update(user_id,
                         f"\n Пользователь запросил файл {media_id}.{file_type}. Путь:'{media_id}.{file_type}'")
    await message.reply_document(
        document=types.FSInputFile(
            path=f"Media/{media_id}.{file_type}",
            filename=f"{name}.{file_type}"
        )
    )

async def delete_file(connection, user_id, media_id, file_type):
    await history_update(user_id,
                         f"\n Пользователь удалил файл. Путь:'Media/{media_id}.{file_type}'")
    await delete_file_media(connection, media_id)
    os.remove(f"Media/{media_id}.{file_type}")
