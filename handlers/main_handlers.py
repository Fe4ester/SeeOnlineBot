from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router
from filters import CommandOrTextFilter
from keyboards import keyboards as kb
from user_functions import database_functions as db
from states import CheckStates

from admin_functions import database_functions

import os
from dotenv import load_dotenv

load_dotenv()

admin_whitelist = int(os.getenv("ADMIN_WHITELIST"))

router = Router()


@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer('Привет! 👋\n'
                         'Я бот для отслеживания активности пользователей 📊.\n'
                         'Теперь у тебя есть возможность следить за тем, кто и когда онлайн ⏰.\n\n'
                         'Больше информации — /help 📚.\n\n'
                         'И да, если ты используешь меня — значит, ты настоящий сталкер! 😎👀', reply_markup=kb.help_kb)


@router.message(CommandOrTextFilter(command='help', text_contains='Информация👩‍💻'))
async def start_command(message: Message):
    await message.answer('🔍 Бот проверяет и записывает посещения пользователя. Можно установить до 5 сеансов проверки.\n\n'
                         '⚠️ Учти: если у пользователя скрыт онлайн, то увидеть его активность не получится.\n\n'
                         '📎 Отправляй как юзернеймы, так и ссылки на пользователей.\n\n'
                         '❓ Если что-то не так — жми /support!', reply_markup=kb.main_kb_1)


@router.message(CommandOrTextFilter(command='back', text_contains='Назад'))
async def back_command(message: Message, state: FSMContext):
    await message.answer('Возвращаюсь...', reply_markup=kb.main_kb_1)
    await state.clear()


@router.message(Command('support'))
async def support_command(message: Message):
    await message.answer('Если возникли какие то проблемы - @Fe4ester')


@router.message(Command('admin'))
async def admin_command(message: Message, state: FSMContext):
    if message.from_user.id != admin_whitelist:
        return

    users = await db.get_all_current_users()

    if not users:
        await message.answer("На данный момент нет отслеживаемых пользователей")
    else:
        await state.update_data(users=users)

        user_list = "\n".join([f"{idx + 1}. {user[0]}" for idx, user in enumerate(users)])
        await message.answer(f"Отслеживаемые пользователи:\n{user_list}")
#         await message.answer("Введите номер пользователя, которого вы хотите удалить:", reply_markup=kb.back_kb)
#
#         await state.set_state(CheckStates.delete)
#
#
# @router.message(CheckStates.delete)
# async def delete_user_by_number(message: Message, state: FSMContext):
#     if not message.text.isdigit():
#         await message.answer("Пожалуйста, введите корректный номер пользователя")
#         await state.clear()
#         return
#
#     data = await state.get_data()
#     users = data.get('users')
#
#     user_number = int(message.text)
#
#     if user_number < 1 or user_number > len(users):
#         await message.answer("Некорректный номер пользователя. Попробуйте снова")
#         return
#
#     user_to_delete = users[user_number - 1][0]
#
#     await db.delete_id_admin(user_to_delete)
#
#     await message.answer(f"Пользователь {user_to_delete} успешно удален из базы данных", reply_markup=kb.main_kb_1)
#
#     await state.clear()
#
#
# @router.message(Command('whitelist'))
# async def whitelist_command(message: Message):
#     if message.from_user.id != admin_whitelist:
#         return
#
#     users = await database_functions.get_whitelist_users()
#
#     if users:
#         user_list = "\n".join([f"{idx + 1}. {user}" for idx, user in enumerate(users)])
#         await message.answer(f"Список пользователей в whitelist:\n{user_list}")
#     else:
#         await message.answer("Whitelist пуст")
#
#
# @router.message(Command('whitelist_add'))
# async def whitelist_add_command(message: Message):
#     if message.from_user.id != admin_whitelist:
#         return
#
#     args = message.text.split()
#     if len(args) == 2:
#         try:
#             target_user_id = int(args[1])
#
#             added = await database_functions.add_user_to_whitelist(target_user_id)
#             if added:
#                 await message.answer(f"Пользователь с ID {target_user_id} успешно добавлен в whitelist")
#             else:
#                 await message.answer(f"Пользователь с ID {target_user_id} уже находится в whitelist")
#         except ValueError:
#             await message.answer("Неверный формат команды. Используйте: /whitelist_add <user_id>")
#     else:
#         await message.answer("Используйте команду в формате: /whitelist_add <user_id>")
#
#
# @router.message(Command('whitelist_remove'))
# async def whitelist_remove_command(message: Message):
#     if message.from_user.id != admin_whitelist:
#         return
#
#     args = message.text.split()
#     if len(args) == 2:
#         try:
#             target_user_id = int(args[1])
#
#             removed = await database_functions.remove_user_from_whitelist(target_user_id)
#             if removed:
#                 await message.answer(f"Пользователь с ID {target_user_id} успешно удален из whitelist")
#             else:
#                 await message.answer(f"Пользователь с ID {target_user_id} не найден в whitelist")
#         except ValueError:
#             await message.answer("Неверный формат команды. Используйте: /whitelist_remove <user_id>")
#     else:
#         await message.answer("Используйте команду в формате: /whitelist_remove <user_id>")
