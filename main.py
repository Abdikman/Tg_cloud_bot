import asyncio
import datetime
import logging
import os
import re
import sys

from aiogram import Bot, Dispatcher, html, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

from Bot_state import file_name_input, file_action
from action import rename_file, file_to_user, delete_file
from Keyboads import keyboard, keyboard2, keyboard3, name_inline_keyboard, MyCallback, name_inline_keyboard_date, \
    MyCallback_for_date, name_inline_keyboard_type, MyCallback_for_type
from download_path import document_path, photo_path, video_path, audio_path
from logging_history import history_update, delete_history

load_dotenv()
dp = Dispatcher()
bot = Bot(token=os.getenv("token"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

type_list = {"document", "photo", "video", "audio"}


@dp.message(Command('start'))
async def command_start_handler(message: Message, state: FSMContext):
    await message.answer(f"Здравствуйте, {html.bold(message.from_user.full_name)}!")
    await message.answer("Для того, чтобы что-нибудь загрузить в облако просто отправьте любой файл")
    await state.clear()
    await state.update_data(user_id=message.from_user.id)
    if f'id_{message.from_user.id}' not in os.listdir():
        os.mkdir(f"id_{message.from_user.id}")


@dp.message(Command('logging_history'))
async def command_history_handler(message: Message, state: FSMContext):
    if f'logging_history.txt' not in os.listdir(f'id_{message.from_user.id}'):
        await delete_history(message.from_user.id)
    await state.clear()
    user_id = message.from_user.id
    with open(f'id_{user_id}/logging_history.txt', 'r', encoding='utf-8') as file:
        if file.read() != '':
            await message.reply(f'{open(f"id_{user_id}/logging_history.txt", "r", encoding="utf-8").read()}')
        else:
            await message.reply('История пуста')


@dp.message(Command('delete_logging_history'))
async def command_delete_history_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(user_id=message.from_user.id)
    await delete_history(message.from_user.id)
    await message.answer('История очищена')


@dp.message(Command('search_file'))
async def command_delete_file(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    if f'id_{message.from_user.id}' not in os.listdir():
        os.mkdir(f"id_{message.from_user.id}")
    await state.set_state(file_action.path_date)
    j = str()
    for i in os.listdir(f'id_{message.from_user.id}/')[:-1]:
        j = j + i + '\n'
    await message.answer(f'Укажите дату, когда файл был загружен:\n{j}')


@dp.message(Command('search_file_name'))
async def command_search_file_name(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(user_id=message.from_user.id)
    await message.answer('Введите название файла')
    await state.set_state(file_action.search_name)


@dp.message(Command('search_file_date'))
async def command_search_file_date(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(user_id=message.from_user.id)
    await message.answer('Введите что известно по дате в формате ****-**-**')
    await state.set_state(file_action.search_date)


@dp.message(Command('search_file_type'))
async def command_search_file_type(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(user_id=message.from_user.id)
    await message.answer('Введите тип искомого файл (Файлы фото всегда сохраняются в jpg):')
    await state.set_state(file_action.search_type)


@dp.message(file_action.path_date)
async def search_path_date(message: Message, state: FSMContext):
    if message.text not in os.listdir(f'id_{message.from_user.id}/'):
        await message.answer('Папки с такой датой нет')
        await state.set_state(file_action.path_date)
    else:
        await state.update_data(path_date=message.text)
        j = str()
        for i in os.listdir(f'id_{message.from_user.id}/{message.text}'):
            j = j + i + '\n'

        await message.answer(f'Укажите тип файла:\n{j}')
        await state.set_state(file_action.path_type)


@dp.message(file_action.path_type)
async def search_path_type(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text.lower() not in os.listdir(f'id_{message.from_user.id}/{data["path_date"]}/'):
        await message.answer('Папки с таким типом расширения нет')
        await state.set_state(file_action.path_type)
    else:
        j = str()
        for i in os.listdir(f'id_{message.from_user.id}/{data["path_date"]}/{message.text.lower()}'):
            j = j + i.split(".")[0] + '\n'
        await state.update_data(path_type=message.text.lower())
        await message.answer(f'Укажите название файла:\n{j}')
        await state.set_state(file_action.file_path)


@dp.message(file_action.file_path)
async def file_path_search(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text + '.' + data["path_type"] not in os.listdir(
            f'id_{message.from_user.id}/{data["path_date"]}/{data["path_type"]}'):
        await message.answer('Такого файла здесь нет')
        await state.set_state(file_action.file_path)
    else:
        await state.update_data(name=message.text)
        await message.answer(text="Что вы хотите сделать с этим файлом?", reply_markup=keyboard3())
        await state.set_state(file_action.action)


@dp.message(file_action.search_name)
async def input_name(message: Message, state: FSMContext):
    list1 = []
    for i in os.listdir(f'id_{message.from_user.id}/')[:-1]:
        for j in os.listdir(f'id_{message.from_user.id}/{i}'):
            for c in os.listdir(f'id_{message.from_user.id}/{i}/{j}'):
                if re.match(message.text.lower(), c.lower()) is not None:
                    list1.append(f'id_{message.from_user.id}/{i}/{j}/{c}')
    if len(list1) == 0:
        await message.answer("Совпадений не найдено, попробуйте снова")
        await state.set_state(file_action.search_name)
    else:
        await state.update_data(list1=list1)
        await message.answer("Выберите какой именно файл вам нужен:", reply_markup=name_inline_keyboard(list1, message.from_user.id))


@dp.message(file_action.search_type)
async def input_type(message: Message, state: FSMContext):
    list1 = []
    for i in os.listdir(f'id_{message.from_user.id}/')[:-1]:
        for j in os.listdir(f'id_{message.from_user.id}/{i}'):
            if re.match(message.text.lower(), j.lower()) is not None:
                list1.append(f'id_{message.from_user.id}/{i}/{j}/')
    if len(list1) == 0:
        await message.answer("Совпадений не найдено, попробуйте снова")
        await state.set_state(file_action.search_name)
    else:
        await state.update_data(list1=list1)
        await message.answer("Выберите какой именно файл вам нужен:",
                             reply_markup=name_inline_keyboard_type(list1, message.from_user.id))


@dp.message(file_action.search_date)
async def input_date(message: Message, state: FSMContext):
    list1 = []
    for i in os.listdir(f'id_{message.from_user.id}/')[:-1]:
        if re.match(message.text.lower(), i.lower()) is not None:
            list1.append(f'id_{message.from_user.id}/{i}')
    if len(list1) == 0:
        await message.answer("Совпадений не найдено, попробуйте снова")
        await state.set_state(file_action.search_date)
    else:
        await state.update_data(list1=list1)
        await message.answer("Выберите какой тип файла вам нужен:",
                             reply_markup=name_inline_keyboard_date(list1, message.from_user.id))


@dp.callback_query(MyCallback.filter())
async def my_callback_name(query: CallbackQuery, callback_data: MyCallback, state: FSMContext):
    await state.update_data(name=callback_data.name,
                            user_id=callback_data.user_id,
                            path_date=callback_data.path_date,
                            path_type=callback_data.path_type)
    await query.message.answer(text="Что вы хотите сделать с этим файлом?", reply_markup=keyboard3())
    await state.set_state(file_action.action)


@dp.callback_query(MyCallback_for_date.filter())
async def my_callback_date(query: CallbackQuery, callback_data: MyCallback_for_date, state: FSMContext):
    await state.update_data(path_date=callback_data.path_date,
                            user_id=callback_data.user_id)
    j = str()
    for i in os.listdir(f'id_{callback_data.user_id}/{callback_data.path_date}'):
        j = j + i + '\n'

    await query.message.answer(f'Укажите тип файла:\n{j}')
    await state.set_state(file_action.path_type)


@dp.callback_query(MyCallback_for_type.filter())
async def my_callback_type(query: CallbackQuery, callback_data: MyCallback_for_type, state: FSMContext):
    await state.update_data(name=callback_data.name,
                            user_id=callback_data.user_id,
                            path_date=callback_data.path_date,
                            path_type=callback_data.path_type)
    j = str()
    for i in os.listdir(f'id_{callback_data.user_id}/{callback_data.path_date}/{callback_data.path_type}'):
        j = j + i + '\n'

    await query.message.answer(text="Что вы хотите сделать с этим файлом?", reply_markup=keyboard3())
    await state.set_state(file_action.action)


@dp.message(file_action.action)
async def file_act(message: Message, state: FSMContext):
    await state.update_data(action=message.text)
    data = await state.get_data()
    match message.text:
        case 'Переименовать':
            await state.set_state(file_action.new_name)
            await message.answer('Введите новое название')
        case 'Скачать':
            await message.answer('Вот ваш файл:')
            await file_to_user(message, data)
            print(f"id_{data['user_id']}/{data['path_date']}/{data['path_type']}/{data['name']}")
            await message.reply_document(
                document=types.FSInputFile(
                    path=f"id_{data['user_id']}/{data['path_date']}/{data['path_type']}/{data['name']}.{data['path_type']}",
                    filename=f"{data['name']}"
                )
            )
            await state.clear()
        case 'Удалить':
            await delete_file(message, data)
            await message.answer(f'Файл {data["name"]} удалён')
            await state.clear()
        case _:
            await message.answer('Такого действия нет. Начните с начала')
            await state.clear()


@dp.message(file_action.new_name)
async def new_name(message: Message, state: FSMContext):
    await state.update_data(new_name=message.text)
    data = await state.get_data()
    await rename_file(message, data)
    await message.answer(f'Файл {data["name"]} переименован в {data["new_name"]} ')


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
            await state.set_state(file_name_input.question)
            await message.answer("Введите название под которым файл будет сохранён")

        if message.photo is not None:
            await state.update_data(file='photo')
            await state.update_data(file_type='jpg')
            file_path = await photo_path(message, bot)
            await state.update_data(file_path=file_path)

            await state.set_state(file_name_input.question)
            await message.answer("Введите название под которым фото будет сохранёно")

        if message.video is not None:
            await state.update_data(file='video')
            await state.update_data(file_type=message.video.file_name.split('.')[1])
            file_path = await video_path(message, bot)
            await state.update_data(file_path=file_path)

            await state.set_state(file_name_input.question)
            await message.answer("Введите название под которым видео будет сохранёно")

        if message.audio is not None:
            await state.update_data(file='audio')
            await state.update_data(file_type=message.audio.file_name.split('.')[1])
            file_path = await audio_path(message, bot)
            await state.update_data(file_path=file_path)

            await state.set_state(file_name_input.question)
            await message.answer("Введите название под которым аудио будет сохранёно")

    except Exception as e:
        print(e)


@dp.message(file_name_input.question)
async def ask(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    data = await state.get_data()
    user_id = message.from_user.id
    day = datetime.date.today()

    if str(day) not in os.listdir(f'id_{user_id}/'):
        os.mkdir(f'id_{user_id}/{day}')
    if data['file_type'] not in os.listdir(f'id_{user_id}/{day}/'):
        os.mkdir(f'id_{user_id}/{day}/{data["file_type"]}')

    if 'question' not in data.keys():
        await state.update_data(question=0)
        data = await state.get_data()

    if data['question'] == 0 and f'{message.text}.{data["file_type"]}' in os.listdir(
            f'id_{user_id}/{day}/{data["file_type"]}/'):
        await state.set_state(file_name_input.all)
        await message.answer("У вас есть файл под таким название. Вы уверены, что хотите заменить его?",
                             reply_markup=keyboard())
        await state.update_data(question=1)
        data = await state.get_data()

    if f'{message.text}.{data["file_type"]}' not in os.listdir(f'id_{user_id}/{day}/{data["file_type"]}/'):
        await state.set_state(file_name_input.name)
        await message.answer(text='Продолжите', reply_markup=keyboard2())


@dp.message(file_name_input.all)
async def answer_question(message: Message, state: FSMContext):
    if message.text == 'Да':
        await message.answer("Замена...")
        await state.set_state(file_name_input.name)
        await state.update_data(question=0)
        await message.answer(text='Продолжите', reply_markup=keyboard2())

    if message.text == 'Нет':
        await message.answer("Напишите другое название")
        await state.update_data(question=0)
        await state.set_state(file_name_input.question)
        await message.answer(text='Продолжите', reply_markup=keyboard2())


@dp.message(file_name_input.name)
async def file_installer(message: Message, state: FSMContext):
    data = await state.get_data()

    user_id = message.from_user.id
    day = datetime.date.today()

    match data['file']:
        case 'document':
            await bot.download_file(data['file_path'],
                                    f"id_{user_id}/{day}/{data['file_type']}/{data['name']}.{data['file_type']}")
            await message.answer("Document received!")
            await history_update(user_id,
                                 f"{day}:\n Пользователь установил файл. Путь:'{day}/{data['file_type']}/{data['name']}.{data['file_type']}'")
        case 'photo':
            await bot.download_file(data['file_path'],
                                    f"id_{user_id}/{day}/{data['file_type']}/{data['name']}.{data['file_type']}")
            await message.answer("Photo received!")
            await history_update(user_id,
                                 f"{day}:\n Пользователь установил фото. Путь:'{day}/{data['file_type']}/{data['name']}.{data['file_type']}'")
        case 'video':
            await bot.download_file(data['file_path'],
                                    f"id_{user_id}/{day}/{data['file_type']}/{data['name']}.{data['file_type']}")
            await message.answer("Video received!")
            await history_update(user_id,
                                 f"{day}:\n Пользователь установил dидео. Путь:'{day}/{data['file_type']}/{data['name']}.{data['file_type']}'")
        case 'audio':
            await bot.download_file(data['file_path'],
                                    f"id_{user_id}/{day}/{data['file_type']}/{data['name']}.{data['file_type']}")
            await message.answer("Audio received!")
            await history_update(user_id,
                                 f"{day}:\n Пользователь установил аудио. Путь:'{day}/{data['file_type']}/{data['name']}.{data['file_type']}'")

    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
