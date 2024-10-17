import aiosqlite
from config import whitelist_path


# Инициализация базы данных и создание таблицы, если ее нет
async def init_whitelist_db():
    async with aiosqlite.connect(whitelist_path) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS whitelist (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER UNIQUE
                            )''')
        await db.commit()


# Проверка, есть ли пользователь в whitelist
async def is_user_in_whitelist(user_id: int):
    async with aiosqlite.connect(whitelist_path) as db:
        cursor = await db.execute("SELECT user_id FROM whitelist WHERE user_id = ?", (user_id,))
        result = await cursor.fetchone()
        return result is not None


# Добавление пользователя в whitelist
async def add_user_to_whitelist(user_id: int):
    async with aiosqlite.connect(whitelist_path) as db:
        try:
            await db.execute("INSERT INTO whitelist (user_id) VALUES (?)", (user_id,))
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            # Пользователь уже в списке
            return False


# Удаление пользователя из whitelist
async def remove_user_from_whitelist(user_id: int):
    async with aiosqlite.connect(whitelist_path) as db:
        cursor = await db.execute("DELETE FROM whitelist WHERE user_id = ?", (user_id,))
        await db.commit()
        # Возвращаем True, если запись была удалена (rowcount > 0), иначе False
        return cursor.rowcount > 0

# Получение списка пользователей из whitelist
async def get_whitelist_users():
    async with aiosqlite.connect(whitelist_path) as db:
        cursor = await db.execute("SELECT user_id FROM whitelist")
        users = await cursor.fetchall()
        return [user[0] for user in users]  # Возвращаем список user_id