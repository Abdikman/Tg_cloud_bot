import os
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

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

class MyCallback_for_search(CallbackData, prefix="my"):
    path_date: str
    path_type: str
    user_id: int

class PaginationCallback_for_name(CallbackData, prefix="pagination"):
    action: str
    page: int

class PaginationCallback_for_date(CallbackData, prefix="pagination_date"):
    action: str
    page: int

class PaginationCallback_for_type(CallbackData, prefix="pagination_type"):
    action: str
    page: int

class PaginationCallback_for_file(CallbackData, prefix="pagination_file"):
    action: str
    page: int

def search_name_inline_keyboard(list1, user_id, page: int, per_page: int = 8):
    builder = InlineKeyboardBuilder()

    start_index = page * per_page
    end_index = start_index + per_page

    for i in list1[start_index:end_index]:
        builder.button(text=i.split('/')[-1],
                       callback_data=MyCallback_for_name(
                           name=i.split('/')[-1].split('.')[0],
                           path_type=i.split('/')[-1].split('.')[1],
                           path_date=i.split('/')[1],
                           user_id=user_id
                       )
                       )

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=PaginationCallback_for_name(action="prev_name", page=page - 1).pack()
                                                       ))
    if end_index < len(list1):
        navigation_buttons.append(InlineKeyboardButton(text="➡️", callback_data=PaginationCallback_for_name(action="next_name", page=page + 1).pack()
                                                       ))

    builder.row(*navigation_buttons)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def search_date_inline_keyboard(list1, user_id, page: int, per_page: int = 8):
    builder = InlineKeyboardBuilder()

    start_index = page * per_page
    end_index = start_index + per_page

    for i in list1[start_index:end_index]:
        builder.button(text=i.split('/')[-1],
                       callback_data=MyCallback_for_date(path_date=i.split('/')[1],
                                                         user_id=user_id))

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=PaginationCallback_for_date(action="prev_date", page=page - 1).pack()
                                 ))
    if end_index < len(list1):
        navigation_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=PaginationCallback_for_date(action="next_date", page=page + 1).pack()
                                 ))

    builder.row(*navigation_buttons)

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def search_type_inline_keyboard(list1, user_id, page: int, per_page: int = 8):
    builder = InlineKeyboardBuilder()

    start_index = page * per_page
    end_index = start_index + per_page
    list2 = []
    for i in list1:
        for j in os.listdir(i):
            list2.append(i+'/'+j)
    print(list2)
    for i in list2[start_index:end_index]:
        builder.button(text=i.split('/')[-1],
                       callback_data=MyCallback_for_type(name=i.split('/')[-1].split('.')[0],
                                                         path_date=i.split('/')[1],
                                                         path_type=i.split('/')[2],
                                                         user_id=user_id))

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=PaginationCallback_for_type(action="prev_type", page=page - 1).pack()
                                 ))
    if end_index < len(list2):
        navigation_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=PaginationCallback_for_type(action="next_type", page=page + 1).pack()
                                 ))

    builder.row(*navigation_buttons)

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def search_file_inline_keyboard(list1, user_id, page: int, per_page: int = 8):
    builder = InlineKeyboardBuilder()

    start_index = page * per_page
    end_index = start_index + per_page

    for i in list1[start_index:end_index]:
        builder.button(text=i.split('/')[-1],
                       callback_data=MyCallback_for_search(path_date=i.split('/')[1],
                                                           path_type=i.split('/')[-1],
                                                           user_id=user_id))

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=PaginationCallback_for_file(action="prev_file", page=page - 1).pack()
                                 ))
    if end_index < len(list1):
        navigation_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=PaginationCallback_for_file(action="next_file", page=page + 1).pack()
                                 ))

    builder.row(*navigation_buttons)

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
