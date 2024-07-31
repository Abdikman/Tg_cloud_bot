from aiogram.utils.keyboard import ReplyKeyboardBuilder


def keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Да')
    builder.button(text='Нет')
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def keyboard2():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Продолжить')
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def keyboard_action():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Переименовать')
    builder.button(text='Скачать')
    builder.button(text='Удалить')
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

