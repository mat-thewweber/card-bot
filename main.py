import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
from database import init_db

from config import BOT_TOKEN
from handlers import callbacks, commands
from handlers import callbacks, commands, feedback

async def set_commands(bot: Bot):
    await init_db()
    await bot.set_my_commands([
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="menu", description="Main menu"),
        BotCommand(command="about", description="About me"),
        BotCommand(command="projects", description="My projects"),
        BotCommand(command="contacts", description="Contacts"),
        BotCommand(command="help", description="Available commands"),
    ])

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True),
    )
    
    dp = Dispatcher()
    dp.include_router(callbacks.router)
    dp.include_router(feedback.router)
    dp.include_router(commands.router)

    await set_commands(bot)
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())