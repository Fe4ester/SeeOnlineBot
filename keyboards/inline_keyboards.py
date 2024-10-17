from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_kb_1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_user')],
    [InlineKeyboardButton(text='Удалить', callback_data='delete_user_menu')],
    [InlineKeyboardButton(text='Просмотреть', callback_data='view_users_menu')]
])

main_kb_2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_user')]
])
back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")]
])


async def generate_hide_kb(username: str):
    inline_keyboard = [
        [InlineKeyboardButton(text="Спрятать", callback_data=f"hide_graph:{username}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def generate_delete_kb(users):
    inline_keyboard = [
        [InlineKeyboardButton(text=user[0], callback_data=f'delete_user:{user[0]}')]
        for user in users
    ]

    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def generate_view_kb(users):
    inline_keyboard = [
        [InlineKeyboardButton(text=user[0], callback_data=f'view_user:{user[0]}')]
        for user in users
    ]

    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def generate_day_kb(username):
    inline_keyboard = [
        [InlineKeyboardButton(text="Сегодня", callback_data=f'view_day:{username}:today')],
        [InlineKeyboardButton(text="Вчера", callback_data=f'view_day:{username}:yesterday')],
        [InlineKeyboardButton(text="Позавчера", callback_data=f'view_day:{username}:day_before_yesterday')],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
