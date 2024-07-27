from Logging_bot.logging_history import history_update
import os
from aiogram import types

async def rename_file(message, data):
    await history_update(message.from_user.id,
                         f"\n Пользователь переименовал файл из {data['name']} в {data['new_name']}. Путь:'{data['path_date']}/{data['path_type']}/{data['new_name']}'")
    os.rename(f"id_{message.from_user.id}/{data['path_date']}/{data['path_type']}/{data['name']}.{data['path_type']}", f"id_{message.from_user.id}/{data['path_date']}/{data['path_type']}/{data['new_name']}.{data['path_type']}")

async def file_to_user(message, data):
    await history_update(message.from_user.id,
                         f"\n Пользователь запросил файл {data['name']}. Путь:'{data['path_date']}/{data['path_type']}/{data['name']}'")
    await message.reply_document(
        document=types.FSInputFile(
            path=f"id_{data['user_id']}/{data['path_date']}/{data['path_type']}/{data['name']}.{data['path_type']}",
            filename=f"{data['name']}"
        )
    )

async def delete_file(message, data):
    await history_update(message.from_user.id,
                         f"\n Пользователь удалил файл. Путь:'{data['path_date']}/{data['path_type']}/{data['name']}'")
    os.remove(f"id_{message.from_user.id}/{data['path_date']}/{data['path_type']}/{data['name']}.{data['path_type']}")
