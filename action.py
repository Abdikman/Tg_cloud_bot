from logging_history import history_update
import os

async def rename_file(message, data):
    await history_update(message.from_user.id,
                         f"{data['path_date']}:\n Пользователь переименовал файл из {data['name']} в {data['new_name']}. Путь:'{data['path_date']}/{data['path_type']}/{data['new_name']}'")
    os.rename(f"id_{message.from_user.id}/{data['path_date']}/{data['path_type']}/{data['name']}.{data['path_type']}", f"id_{message.from_user.id}/{data['path_date']}/{data['path_type']}/{data['new_name']}.{data['path_type']}")

async def file_to_user(message, data):
    await history_update(message.from_user.id,
                         f"{data['path_date']}:\n Пользователь запросил файл {data['name']}. Путь:'{data['path_date']}/{data['path_type']}/{data['name']}'")

async def delete_file(message, data):
    await history_update(message.from_user.id,
                         f"{data['path_date']}:\n Пользователь удалил файл. Путь:'{data['path_date']}/{data['path_type']}/{data['name']}'")
    os.remove(f"id_{message.from_user.id}/{data['path_date']}/{data['path_type']}/{data['name']}.{data['path_type']}")
