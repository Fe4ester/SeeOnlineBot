from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb_1 = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Главное меню')]
], resize_keyboard=True)

back_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад')]
], resize_keyboard=True)

help_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Информация👩‍💻')]
], resize_keyboard=True, input_field_placeholder='Жми, кнопка одна...')

yn_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Да'), KeyboardButton(text='Нет')]
], resize_keyboard=True)

stop_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Стоп')]
], resize_keyboard=True)


