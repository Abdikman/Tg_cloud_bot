import asyncio
import datetime
import logging
import os
import sys

from aiogram import Bot, Dispatcher, html, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

from Bot_states.bot_state import bot_download_states, file_action
from Handles.action import rename_file, file_to_user, delete_file
from Handles.sql_command import insert_file, select_files, select_file_id, delete_file_media, select_file_where, \
    update_file_description
from Keyboards.Keyboads import keyboard, keyboard_action
from Keyboards.Inline_keyboard import search_date_inline_keyboard, \
    MyCallback_for_date, search_file_inline_keyboard, MyCallback_for_file, search_type_inline_keyboard, \
    MyCallback_for_type, PaginationCallback_for_date, PaginationCallback_for_file, \
    PaginationCallback_for_type
from Handles.download_path import document_path, photo_path, video_path, audio_path
from Logging_bot.logging_history import history_update, delete_history
from SQLite.sql_start import create_connection

load_dotenv("config/.env")
dp = Dispatcher()
bot = Bot(token=os.getenv("token"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

type_list = {"document", "photo", "video", "audio"}


@dp.message(Command('start'))
async def command_start_handler(message: Message, state: FSMContext):
    await message.answer(f"Здравствуйте, {html.bold(message.from_user.full_name)}!")
    await message.answer("Для того, чтобы что-нибудь загрузить в облако просто отправьте любой файл")
    await state.clear()
    await state.update_data(user_id=message.from_user.id)
    if f'Media' not in os.listdir():
        os.mkdir(f"Media")


@dp.message(Command('logging_history'))
async def command_history_handler(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    if f'{user_id}.log' not in os.listdir(f'User_logging'):
        await delete_history(message.from_user.id)

    with open(f'User_logging/{user_id}.log', 'r', encoding='utf-8') as file:
        if file.read() != '':
            await message.reply_document(document=types.FSInputFile(path=f"User_logging/{user_id}.log", filename=f"logging_history.log"))
        else:
            await message.reply('История пуста')

@dp.message(Command('delete_logging_history'))
async def command_delete_history_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(user_id=message.from_user.id)
    await delete_history(message.from_user.id)
    await message.answer('История очищена')


@dp.message(Command('search_file'))
async def command_search_file(message: Message, state: FSMContext):
    await state.clear()
    list1 = []
    page = 0

    where = f"user_id = {message.from_user.id}"
    data_media = await select_file_where(connection, where)

    for i in data_media:
        list1.append(i[3])
    list1 = list(set(list1))

    await state.update_data(list1=list1)
    await message.answer("Выберите какой даты файл вам нужен:",
                         reply_markup=search_date_inline_keyboard(list1, message.from_user.id, page))

@dp.message(Command('search_file_name'))
async def command_search_file_name(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(user_id=message.from_user.id)
    page = 0

    where = f"user_id = {message.from_user.id}"
    data_media = await select_file_where(connection, where)

    await message.answer("Выберите какой файл вам нужен:",
                         reply_markup=search_file_inline_keyboard(data_media, page))
    await state.set_state(file_action.action)

@dp.message(Command('search_file_date'))
async def command_search_file_date(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(search_date=1)
    list1 = []
    page = 0

    where = f"user_id = {message.from_user.id}"
    data_media = await select_file_where(connection, where)

    for i in data_media:
        list1.append(i[3])
    list1 = list(set(list1))

    await state.update_data(list1=list1)
    await message.answer("Выберите какой даты файл вам нужен:",
                         reply_markup=search_date_inline_keyboard(list1, message.from_user.id, page))

@dp.message(Command('search_file_type'))
async def command_search_file_type(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(user_id=message.from_user.id)
    list1 = []
    page = 0

    where = f"user_id = {message.from_user.id}"
    data_media = await select_file_where(connection, where)

    for i in data_media:
        list1.append(i[-1])
    list1 = list(set(list1))

    await message.answer("Выберите какой тип файла вам нужен:",
                         reply_markup=search_type_inline_keyboard(list1, message.from_user.id, page))


@dp.callback_query(PaginationCallback_for_date.filter())
async def handle_pagination(callback: CallbackQuery, callback_data: PaginationCallback_for_date, state: FSMContext):
    page = callback_data.page
    data = await state.get_data()

    await callback.message.edit_reply_markup(
        reply_markup=search_date_inline_keyboard(data['list1'], callback.from_user.id, page))
    await callback.answer()

@dp.callback_query(PaginationCallback_for_file.filter())
async def handle_pagination(callback: CallbackQuery, callback_data: PaginationCallback_for_file, state: FSMContext):
    page = callback_data.page
    data = await state.get_data()
    where = f"user_id = {callback.from_user.id}"

    if "path_date" in data:
        where = where + f" AND date = '{data['path_date']}'"
    if "path_type" in data:
        where = where + f" AND media_type = '{data['path_type']}'"
    data_media = await select_file_where(connection, where)

    await callback.message.edit_reply_markup(
        reply_markup=search_file_inline_keyboard(data_media, page))
    await callback.answer()

@dp.callback_query(PaginationCallback_for_type.filter())
async def handle_pagination(callback: CallbackQuery, callback_data: PaginationCallback_for_type, state: FSMContext):
    list1 = []

    page = callback_data.page
    data = await state.get_data()

    where = f"user_id = {data['user_id']}"
    data_media = await select_file_where(connection, where)

    for i in data_media:
        list1.append(i[-1])
    list1 = list(set(list1))

    await callback.message.edit_reply_markup(
        reply_markup=search_type_inline_keyboard(list1, data['user_id'], page))


@dp.callback_query(MyCallback_for_date.filter())
async def my_callback_date(query: CallbackQuery, callback_data: MyCallback_for_date, state: FSMContext):
    await state.update_data(path_date=callback_data.path_date,
                            user_id=callback_data.user_id)
    data = await state.get_data()
    list1 = []
    page = 0

    where = f"user_id = {callback_data.user_id} AND date = '{callback_data.path_date}'"
    data_media = await select_file_where(connection, where)

    if "search_date" in data:
        await query.message.answer("Выберите какой файл вам нужен:",
                                   reply_markup=search_file_inline_keyboard(data_media, page))
    else:
        for i in data_media:
            list1.append(i[-1])
        list1 = list(set(list1))

        await state.update_data(list1=list1)
        await query.message.answer("Выберите какой тип файла вам нужен:",
                                   reply_markup=search_type_inline_keyboard(list1, query.from_user.id, page))

@dp.callback_query(MyCallback_for_file.filter())
async def my_callback_type(query: CallbackQuery, callback_data: MyCallback_for_file, state: FSMContext):
    await state.update_data(media_id=callback_data.media_id,
                            user_id=query.from_user.id)

    await query.message.answer(text="Что вы хотите сделать с этим файлом?",
                               reply_markup=keyboard_action())
    await state.set_state(file_action.action)

@dp.callback_query(MyCallback_for_type.filter())
async def my_callback_search(query: CallbackQuery, callback_data: MyCallback_for_type, state: FSMContext):
    await state.update_data(path_type=callback_data.path_type)
    page = 0
    data = await state.get_data()

    where = f"user_id = {query.from_user.id} AND media_type = '{callback_data.path_type}'"
    if "path_date" in data:
        where = where + f" AND date = '{data['path_date']}'"
    data_media = await select_file_where(connection, where)

    await query.message.answer("Выберите какой именно файл вам нужен:",
                               reply_markup=search_file_inline_keyboard(data_media, page))
    await state.set_state(file_action.action)


@dp.message(file_action.action)
async def file_act(message: Message, state: FSMContext):
    data = await state.get_data()

    where = f"id = {data['media_id']}"
    data_media = await select_file_where(connection, where)
    data_media = data_media[0]

    match message.text:
        case 'Переименовать':
            await state.set_state(file_action.new_name)
            await message.answer('Введите новое название')
        case 'Посмотреть описание':
            await message.answer(f'Описание к файлу:\n{data_media[2]}')
            await state.set_state(file_action.question)
            await message.answer(f'Хотите изменить описание файла?', reply_markup=keyboard())
        case 'Скачать':
            await message.answer('Вот ваш файл:')
            await file_to_user(message, data_media[1], message.from_user.id, data_media[0], data_media[-1])
            await message.answer(f'Описание к файлу:\n{data_media[2]}')
            await state.clear()
        case 'Удалить':
            await delete_file(connection, message.from_user.id, data_media[0], data_media[-1])
            await message.answer(f'Файл {data_media[1]}.{data_media[-1]} удалён')
            await state.clear()
        case _:
            await message.answer('Такого действия нет. Начните с начала')
            await state.clear()

@dp.message(file_action.new_name)
async def new_name(message: Message, state: FSMContext):
    data = await state.get_data()

    where = f"id = {data['media_id']}"
    data_media = await select_file_where(connection, where)
    data_media = data_media[0]

    await rename_file(connection, data_media[1], message.text, message.from_user.id, data_media[0], data_media[-1])
    await message.answer(f'Файл {data_media[1]} переименован в {message.text}')

@dp.message(file_action.question)
async def description_question(message: Message, state: FSMContext):
    if message.text == 'Да':
        await message.answer("Введите описание для файла")
        await state.set_state(file_action.new_description)

    if message.text == 'Нет':
        await message.answer("Ну ок")
        await state.clear()


@dp.message(file_action.new_description)
async def new_description(message: Message, state: FSMContext):
    data = await state.get_data()
    where = f"id = {data['media_id']}"
    data_media = await select_file_where(connection, where)
    data_media = data_media[0]

    await update_file_description(connection, data['media_id'], message.text)
    await message.answer(f'У файла {data_media[1]} поменялось описание на:')
    await message.answer(f'"{message.text}"')
    await state.clear()


@dp.message(F.content_type.in_(type_list))
async def document_handler(message: Message, state: FSMContext):
    try:
        if message.document is not None:
            await state.update_data(file='document')
            """Сохраняем file_path для установки документа"""
            file_path = await document_path(message, bot)
            await state.update_data(file_path=file_path)

            """Сохраняем расширение файла"""
            file_type = message.document.file_name.split('.')[1]
            await state.update_data(file_type=file_type)

            """Спрашиваем у пользователя название файла для сохранения"""
            await state.set_state(bot_download_states.input_name)
            await message.answer("Введите название под которым файл будет сохранён")

        if message.photo is not None:
            await state.update_data(file='photo')
            await state.update_data(file_type='jpg')
            file_path = await photo_path(message, bot)
            await state.update_data(file_path=file_path)

            await state.set_state(bot_download_states.input_name)
            await message.answer("Введите название под которым файл будет сохранёно")

        if message.video is not None:
            await state.update_data(file='video')
            await state.update_data(file_type=message.video.file_name.split('.')[1])
            file_path = await video_path(message, bot)
            await state.update_data(file_path=file_path)

            await state.set_state(bot_download_states.input_name)
            await message.answer("Введите название под которым файл будет сохранёно")

        if message.audio is not None:
            await state.update_data(file='audio')
            await state.update_data(file_type=message.audio.file_name.split('.')[1])
            file_path = await audio_path(message, bot)
            await state.update_data(file_path=file_path)

            await state.set_state(bot_download_states.input_name)
            await message.answer("Введите название под которым файл будет сохранёно")

    except Exception as e:
        print(e)


@dp.message(bot_download_states.input_name)
async def ask(message: Message, state: FSMContext):
    data = await state.get_data()

    name = message.text
    date = datetime.date.today()
    user_id = message.from_user.id
    media_type = data['file_type']
    await state.update_data(name=name)

    result_media = await select_files(connection, name, date, user_id, media_type)
    count = 0
    if len(result_media) == '[]':
        result_media.append('')
    for i in result_media:
        if name.lower() in i[1].lower():
            count += 1


    if count > 0:
        await state.update_data(file_id_media=result_media[0][0])
        await state.set_state(bot_download_states.all)
        await message.answer("У вас есть файл под таким название. Вы уверены, что хотите заменить его?",
                             reply_markup=keyboard())
    else:
        await state.set_state(bot_download_states.input_description)
        await message.answer("Введите описание для файла")

@dp.message(bot_download_states.input_description)
async def file_installer(message: Message, state: FSMContext):
    data = await state.get_data()

    name = data['name']
    description = message.text
    date = datetime.date.today()
    user_id = message.from_user.id
    media_type = data['file_type']

    await insert_file(name, description, date, user_id, media_type, connection)
    result_media = await select_file_id(connection, name, description, date, user_id, media_type)

    for i in result_media:
        if i[1].lower() == name.lower():
            await bot.download_file(data['file_path'], f"Media/{i[0]}.{i[-1]}")
            await history_update(user_id, f"\n Пользователь установил файл. Путь:'Media/{i[0]}.{i[-1]}'")

    await message.answer("File received!")
    await state.clear()

@dp.message(bot_download_states.all)
async def answer_question(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'Да':
        await message.answer("Замена...")
        await delete_file_media(connection, data['media_id'])
        await delete_file(connection, message.from_user.id, data['media_id'], data['file_type'])

        await state.set_state(bot_download_states.input_description)
        await message.answer("Введите описание для файла")

    if message.text == 'Нет':
        await message.answer("Напишите другое название")
        await state.set_state(bot_download_states.input_name)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    if 'Media' not in os.listdir():
        os.mkdir('Media')
    if 'bd.sqlite' not in os.listdir('SQlite/'):
        connection = asyncio.run(create_connection(True))
    else:
        connection = asyncio.run(create_connection(False))
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
