from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


class MyCallback_for_date(CallbackData, prefix="search_date"):
    path_date: str
    user_id: int

class MyCallback_for_file(CallbackData, prefix="search_type"):
    media_id: str

class MyCallback_for_type(CallbackData, prefix="search"):
    path_type: str
    user_id: int



class PaginationCallback_for_date(CallbackData, prefix="pagination_date"):
    action: str
    page: int

class PaginationCallback_for_file(CallbackData, prefix="pagination_type"):
    action: str
    page: int

class PaginationCallback_for_type(CallbackData, prefix="pagination_file"):
    action: str
    page: int


def search_date_inline_keyboard(list1, user_id, page: int, per_page: int = 8):
    builder = InlineKeyboardBuilder()

    start_index = page * per_page
    end_index = start_index + per_page
    list1.sort()

    for i in list1[start_index:end_index]:
        builder.button(text=i,
                       callback_data=MyCallback_for_date(path_date=i,
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
    list1.sort()

    for i in list1[start_index:end_index]:
        builder.button(text=i,
                       callback_data=MyCallback_for_type(path_type=i,
                                                         user_id=user_id))

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=PaginationCallback_for_type(action="prev_date", page=page - 1).pack()
                                 ))
    if end_index < len(list1):
        navigation_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=PaginationCallback_for_type(action="next_date", page=page + 1).pack()
                                 ))

    builder.row(*navigation_buttons)

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)



def search_file_inline_keyboard(data_media, page: int, per_page: int = 8):
    builder = InlineKeyboardBuilder()
    start_index = page * per_page
    end_index = start_index + per_page

    for i in data_media[start_index:end_index]:
        text = i[1] + '.' + i[-1]
        builder.button(text=text,
                       callback_data=MyCallback_for_file(media_id=f'{i[0]}'))

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=PaginationCallback_for_file(action="prev_type", page=page - 1).pack()
                                 ))
    if end_index < len(data_media):
        navigation_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=PaginationCallback_for_file(action="next_type", page=page + 1).pack()
                                 ))

    builder.row(*navigation_buttons)

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
