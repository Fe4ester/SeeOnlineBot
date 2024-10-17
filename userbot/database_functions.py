async def load_users_from_db(db):
    cursor = await db.execute("SELECT username, interval FROM users_to_monitor")
    rows = await cursor.fetchall()
    return [{"username": row[0], "interval": row[1]} for row in rows]


async def delete_user_table(username, db):
    await db.execute(f"DROP TABLE IF EXISTS {username}_status_history")
    await db.commit()
    print(f"Deleted history table for user {username}")


async def get_last_status(username, db):
    cursor = await db.execute(f"SELECT status FROM {username}_status_history ORDER BY timestamp DESC LIMIT 1")
    row = await cursor.fetchone()
    return row[0] if row else None
