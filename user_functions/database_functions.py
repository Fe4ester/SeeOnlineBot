import aiosqlite
from aiogram.types import Message
from datetime import datetime
from config import check_online_path


# Функция создания таблицы, если она не существует
async def create_table_users_to_monitor():
    async with aiosqlite.connect(check_online_path) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users_to_monitor 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, interval INTEGER, user_id INTEGER)''')
        await db.commit()


# Получение списка отслеживаемых пользователей для конкретного user_id
async def get_current_users(user_id):
    async with aiosqlite.connect(check_online_path) as db:
        async with db.execute('SELECT username FROM users_to_monitor WHERE user_id = ?', (user_id,)) as cursor:
            return await cursor.fetchall()


# Получение списка всех отслеживаемых пользователей
async def get_all_current_users():
    async with aiosqlite.connect(check_online_path) as db:
        async with db.execute('SELECT username FROM users_to_monitor') as cursor:
            return await cursor.fetchall()


# Сохранение нового пользователя для отслеживания
async def save_id(message: Message, username: str, interval: int):
    async with aiosqlite.connect(check_online_path) as db:
        await db.execute(
            "INSERT INTO users_to_monitor (username, interval, user_id) VALUES (?, ?, ?)",
            (username, interval, message.from_user.id)
        )
        await db.commit()


# Удаление пользователя из отслеживания
async def delete_id(user_id: int, username: str):
    async with aiosqlite.connect(check_online_path) as db:
        await db.execute('DELETE FROM users_to_monitor WHERE user_id = ? AND username = ?', (user_id, username))
        await db.commit()


# Удаление пользователя из отслеживания без проверки прав(для админов)
async def delete_id_admin(username: str):
    async with aiosqlite.connect(check_online_path) as db:
        await db.execute('DELETE FROM users_to_monitor WHERE username = ?', (username, ))
        await db.commit()


# Проверка, отслеживается ли указанный username
async def is_user_monitored(username: str) -> bool:
    async with aiosqlite.connect(check_online_path) as db:
        cursor = await db.execute("SELECT 1 FROM users_to_monitor WHERE username = ?", (username,))
        result = await cursor.fetchone()
        return result is not None


# Получение периодов онлайна пользователя
async def get_online_periods(username: str):
    periods_by_day = {}

    async with aiosqlite.connect(check_online_path) as db:
        query = f"SELECT status, timestamp FROM {username}_status_history ORDER BY timestamp"
        async with db.execute(query) as cursor:
            records = await cursor.fetchall()

            online_start = None

            for status, timestamp in records:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                day = timestamp.date()

                if status not in ['online', 'offline']:
                    return False

                if status == 'online' and not online_start:
                    online_start = timestamp

                elif status == 'offline' and online_start:
                    periods_by_day.setdefault(day, []).append((online_start.time(), timestamp.time()))
                    online_start = None

            if online_start:
                current_time = datetime.now()
                day = online_start.date()
                periods_by_day.setdefault(day, []).append((online_start.time(), current_time.time()))

    return periods_by_day


