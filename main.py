import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeChat

from config import ADMIN_ID, BOT_TOKEN
from database import init_db
from handlers import admin, callbacks, commands, feedback


async def set_commands(bot: Bot):
    user_commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="menu", description="Main menu"),
        BotCommand(command="about", description="About me"),
        BotCommand(command="projects", description="My projects"),
        BotCommand(command="contacts", description="Contacts"),
        BotCommand(command="help", description="Available commands"),
    ]
    await bot.set_my_commands(user_commands)
    await bot.set_my_commands(
        user_commands + [BotCommand(command="stats", description="Statistics")],
        scope=BotCommandScopeChat(chat_id=ADMIN_ID),
    )


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True),
    )
    dp = Dispatcher()
    dp.include_router(callbacks.router)
    dp.include_router(admin.router)
    dp.include_router(feedback.router)
    dp.include_router(commands.router)

    await init_db()
    await set_commands(bot)
    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())