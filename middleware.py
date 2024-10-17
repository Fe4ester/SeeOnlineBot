from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from admin_functions import database_functions
import asyncio

import os
from dotenv import load_dotenv

load_dotenv()

admin_whitelist = int(os.getenv("ADMIN_WHITELIST"))


# class WhitelistMiddleware(BaseMiddleware):
#     async def __call__(self, handler, event: TelegramObject, data: dict):
#         user_id = None
#
#         if isinstance(event, Message):
#             user_id = event.from_user.id
#         elif isinstance(event, CallbackQuery):
#             user_id = event.from_user.id
#
#         if user_id and await database_functions.is_user_in_whitelist(user_id):
#             return await handler(event, data)
#         else:
#             if isinstance(event, Message):
#                 await event.answer(
#                     "Извините, у вас нет доступа к этому боту, что бы получить доступ, можете поболтать с @Fe4ester"
#                 )
#             elif isinstance(event, CallbackQuery):
#                 await event.answer(
#                     "Извините, у вас нет доступа к этому боту, что бы получить доступ, можете поболтать с @Fe4ester",
#                     show_alert=True
#                 )
#
#             return


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, limit: int):
        self.limit = limit
        self.users = {}
        super().__init__()

    async def __call__(self, handler, event, data: dict):
        user_id = None

        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id

        if user_id and user_id == admin_whitelist:
            return await handler(event, data)

        if user_id:
            current_time = asyncio.get_event_loop().time()
            last_time = self.users.get(user_id, 0)

            if current_time - last_time < self.limit:
                if isinstance(event, Message):
                    await event.answer("Пожалуйста, не спамьте!")
                elif isinstance(event, CallbackQuery):
                    await event.answer("Пожалуйста, не спамьте!", show_alert=True)
                return

            self.users[user_id] = current_time

        return await handler(event, data)
