import asyncio
from aiogram import Bot, Dispatcher
from middleware import AntiFloodMiddleware
# from middleware import WhitelistMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import main_handlers
from handlers import check_online_handlers
from callbacks import check_online_callbacks
from admin_functions import database_functions

import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main():
    dp.include_routers(main_handlers.router, check_online_handlers.router, check_online_callbacks.router)
    # dp.message.middleware(WhitelistMiddleware())
    dp.message.middleware(AntiFloodMiddleware(limit=1))

    await database_functions.init_whitelist_db()

    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Error occurred: {e}")
        await asyncio.sleep(5)
        await main()


if __name__ == '__main__':
    while True:
        try:
            print('Working...')
            asyncio.run(main())
        except (KeyboardInterrupt, SystemExit):
            print('Bot stopped.')
            break
        except Exception as e:
            print(f'Unhandled error: {e}. Restarting...')
            asyncio.sleep(5)
