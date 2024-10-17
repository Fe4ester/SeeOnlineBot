from pyrogram import Client
import os
from dotenv import load_dotenv

load_dotenv()

userbot_id = int(os.getenv("USERBOT_ID"))
userbot_hash = os.getenv("USERBOT_HASH")

app = Client("main_account", api_id=userbot_id, api_hash=userbot_hash)

app.run()
