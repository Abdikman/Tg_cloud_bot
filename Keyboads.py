import os
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Да')
    builder.button(text='Нет')
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def keyboard2():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Продолжить')
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def keyboard3():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Переименовать')
    builder.button(text='Скачать')
    builder.button(text='Удалить')
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

class MyCallback(CallbackData, prefix="my"):
    name: str
    user_id: int
    path_type: str
    path_date: str

class MyCallback_for_date(CallbackData, prefix="my"):
    path_date: str
    user_id: int


class MyCallback_for_type(CallbackData, prefix="my"):
    name: str
    path_date: str
    path_type: str
    user_id: int

def name_inline_keyboard(list1, user_id):
    builder = InlineKeyboardBuilder()
    for i in list1:
        builder.button(text=i.split('/')[-1],
                       callback_data=MyCallback(name=i.split('/')[-1].split('.')[0],
                                                path_type=i.split('/')[-1].split('.')[1],
                                                path_date=i.split('/')[1],
                                                user_id=user_id))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def name_inline_keyboard_date(list1, user_id):
    builder = InlineKeyboardBuilder()
    for i in list1:
        builder.button(text=i.split('/')[-1].split('.')[0],
                       callback_data=MyCallback_for_date(path_date=i.split('/')[1],
                                                         user_id=user_id))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def name_inline_keyboard_type(list1, user_id):
    builder = InlineKeyboardBuilder()
    for i in list1:
        for j in os.listdir(i):
            builder.button(text=j,
                           callback_data=MyCallback_for_type(name=j.split('.')[0],
                                                             path_date=i.split('/')[1],
                                                             path_type=i.split('/')[2],
                                                             user_id=user_id))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
