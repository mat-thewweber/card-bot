import asyncio

from database import init_db
from repo import add_project

async def seed():
    await init_db()
    await add_project("Business card bot", "Telegram bot on aiogram 3 with menu, commands and SQLite database")
    print("done")

asyncio.run(seed())