from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, ReplyKeyboardMarkup


def keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Да')
    builder.button(text='Нет')
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def keyboard_action():
    builder = ReplyKeyboardBuilder().add(KeyboardButton(text='Посмотреть описание'))
    builder.row(KeyboardButton(text='Переименовать'))
    builder.row(KeyboardButton(text='Скачать'), KeyboardButton(text='Удалить'))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

