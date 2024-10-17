import asyncio
import aiosqlite
import signal
from pyrogram import Client
from pyrogram.enums import UserStatus
import time
from config import check_online_path
from database_functions import *

app = Client("main_account")
tasks = {}


async def stop_all_users():
    print("Остановка программы. Проверяем статусы для записи 'offline'.")

    async with aiosqlite.connect(check_online_path) as db:
        users_data = await load_users_from_db(db)

        for user_data in users_data:
            username = user_data['username']

            last_status = await get_last_status(username, db)

            if last_status == 'online':
                print(f"Записываем offline для {username}, так как последний статус был online")
                await db.execute(f"INSERT INTO {username}_status_history (status) VALUES (?)", ('offline',))
                await db.commit()
            else:
                print(f"Для {username} запись offline не требуется, так как последний статус был {last_status}")

    for task in tasks.values():
        task.cancel()

    await app.stop()
    print("Pyrogram client stopped.")


async def check_user_status(username, interval, db):
    await db.execute(f'''
        CREATE TABLE IF NOT EXISTS {username}_status_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT,
            timestamp DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
        )
    ''')
    await db.commit()

    last_status = await get_last_status(username, db)

    while True:
        try:
            user = await app.get_users(username)
            status = user.status

            if status == UserStatus.ONLINE:
                status = 'online'
            elif status == UserStatus.OFFLINE:
                status = 'offline'
            else:
                status = 'unknown'

            print(f"User {username} status: {status} (Interval: {interval}s)")

            if status != last_status:
                await db.execute(f"INSERT INTO {username}_status_history (status) VALUES (?)", (status,))
                await db.commit()
                last_status = status

        except Exception as e:
            print(f"Error while checking status for {username}: {e}")
            await asyncio.sleep(5)

        await asyncio.sleep(interval)


async def monitor_users(db):
    global tasks
    while True:
        try:
            users_data = await load_users_from_db(db)
            current_usernames = {user['username'] for user in users_data}

            for user_data in users_data:
                username = user_data['username']
                interval = user_data['interval']

                if username not in tasks:
                    tasks[username] = asyncio.create_task(check_user_status(username, interval, db))
                else:
                    if tasks[username].get_coro().cr_frame.f_locals['interval'] != interval:
                        tasks[username].cancel()
                        tasks[username] = asyncio.create_task(check_user_status(username, interval, db))

            for username in list(tasks.keys()):
                if username not in current_usernames:
                    tasks[username].cancel()
                    del tasks[username]
                    await delete_user_table(username, db)

            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error in user monitoring loop: {e}")
            await asyncio.sleep(5)


async def main():
    async with aiosqlite.connect(check_online_path) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users_to_monitor 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, interval INTEGER, user_id INTEGER)''')
        await db.commit()

        async with app:
            await monitor_users(db)


def shutdown(signal, frame):
    print("Shutdown signal received.")
    loop = asyncio.get_event_loop()
    loop.create_task(stop_all_users())


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Restarting due to an error: {e}")
        time.sleep(5)
