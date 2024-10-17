import re
from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext
from states import CheckStates
from filters import CommandOrTextFilter
from user_functions import database_functions as db

from config import check_interval

from keyboards import inline_keyboards as ikb

import os
from dotenv import load_dotenv

load_dotenv()

admin_whitelist = int(os.getenv("ADMIN_WHITELIST"))

USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9_]+$')

router = Router()


@router.message(CheckStates.set)
async def set_username(message: Message, state: FSMContext):
    username = message.text
    if username.startswith('https://t.me/'):
        username = username[len('https://t.me/'):]
    elif username.startswith('@'):
        username = username[1:]

    if len(username) < 5:
        await message.answer('Слишком короткий юзернейм, введите снова')
        return
    elif len(username) > 32:
        await message.answer('Слишком длинный юзернейм, введите снова')
        return

    if not USERNAME_REGEX.match(username):
        await message.answer('Юзернейм должен содержать только латинские буквы, цифры и подчеркивания. Введите снова')
        return

    if message.from_user.id != admin_whitelist:
        current_users = await db.get_current_users(message.from_user.id)
        if len(current_users) >= 5:
            await message.answer(
                'Вы не можете отслеживать больше 5 юзернеймов. Удалите некоторые из них перед добавлением новых')
            return

    await db.save_id(message, username, check_interval)
    await message.answer('Успешно сохранено')

    monitored_users = await db.get_current_users(message.from_user.id)

    if monitored_users:
        user_list = '\n'.join([f"{idx + 1}. @{user[0]}" for idx, user in enumerate(monitored_users)])
        await message.answer(f"Вы отслеживаете следующих пользователей:\n{user_list}", reply_markup=ikb.main_kb_1)
    else:
        await message.answer('Вы никого не отслеживаете, добавить?', reply_markup=ikb.main_kb_2)
    await state.clear()


@router.message(CommandOrTextFilter(command='list', text_contains='Главное меню'))
async def periods_list_command(message: Message):
    monitored_users = await db.get_current_users(message.from_user.id)

    if monitored_users:
        user_list = '\n'.join([f"{idx + 1}. @{user[0]}" for idx, user in enumerate(monitored_users)])
        await message.answer(f"Вы отслеживаете следующих пользователей:\n{user_list}", reply_markup=ikb.main_kb_1)


    else:
        await message.answer('Вы никого не отслеживаете, добавить?', reply_markup=ikb.main_kb_2)
