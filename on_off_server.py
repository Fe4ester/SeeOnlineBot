import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
# from middleware import WhitelistMiddleware
from aiogram.fsm.storage.memory import MemoryStorage

import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message()
async def on_message(message: Message):
    await message.answer('Извините, ведутся технические работы на сервере, попробуйте позже')


async def main():

    # dp.message.middleware(WhitelistMiddleware())

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

