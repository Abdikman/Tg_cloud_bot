import os
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

class MyCallback_for_name(CallbackData, prefix="my"):
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

def search_name_inline_keyboard(list1, user_id):
    builder = InlineKeyboardBuilder()
    for i in list1:
        builder.button(text=i.split('/')[-1],
                       callback_data=MyCallback_for_name(name=i.split('/')[-1].split('.')[0],
                                                         path_type=i.split('/')[-1].split('.')[1],
                                                         path_date=i.split('/')[1],
                                                         user_id=user_id))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def search_date_inline_keyboard(list1, user_id):
    builder = InlineKeyboardBuilder()
    for i in list1:
        builder.button(text=i.split('/')[-1],
                       callback_data=MyCallback_for_date(path_date=i.split('/')[1],
                                                         user_id=user_id))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def search_type_inline_keyboard(list1, user_id):
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