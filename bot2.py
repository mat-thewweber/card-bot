import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True),
)
dp = Dispatcher()

ABOUT_TEXT = (
    "Hello! My name is Matthew.\n"
    "I'm studying at university and I love to create bots.\n"
    "I have experience in Python."
)
PROJECTS_TEXT = "<b>My projects</b>\n• Business card bot (this one)"
MENU_TEXT = "Choose a section:"


def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 About me", callback_data="about"),
            InlineKeyboardButton(text="💻 Projects", callback_data="projects"),
        ],
        [InlineKeyboardButton(text="📬 Contacts", callback_data="contacts")],
    ])


def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back", callback_data="menu")],
    ])


def contacts_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Telegram", url="https://t.me/Matthew7702")],
        [InlineKeyboardButton(text="🧵 Threads", url="https://www.threads.net/@mat.thewweber")],
        [InlineKeyboardButton(text="💻 GitHub", url="https://github.com/your_github")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="menu")],
    ])


async def set_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="menu", description="Main menu"),
        BotCommand(command="about", description="About me"),
        BotCommand(command="projects", description="My projects"),
        BotCommand(command="contacts", description="Contacts"),
        BotCommand(command="help", description="Available commands"),
    ])


# COMMANDS
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Hello, {message.from_user.full_name}!\n{MENU_TEXT}",
        reply_markup=main_menu_kb(),
    )


@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    await message.answer(MENU_TEXT, reply_markup=main_menu_kb())


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "I'm Matthew's business card bot.\n"
        "Available commands:\n"
        "/start - Start the bot\n"
        "/menu - Main menu\n"
        "/about - About me\n"
        "/projects - My projects\n"
        "/contacts - Contacts"
    )


@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    await message.answer(ABOUT_TEXT, reply_markup=back_kb())


@dp.message(Command("projects"))
async def cmd_projects(message: types.Message):
    await message.answer(PROJECTS_TEXT, reply_markup=back_kb())


@dp.message(Command("contacts"))
async def cmd_contacts(message: types.Message):
    await message.answer("Contacts:", reply_markup=contacts_kb())


# INLINE BUTTONS
@dp.callback_query(F.data == "menu")
async def cb_menu(call: types.CallbackQuery):
    await call.message.edit_text(MENU_TEXT, reply_markup=main_menu_kb())
    await call.answer()


@dp.callback_query(F.data == "about")
async def cb_about(call: types.CallbackQuery):
    await call.message.edit_text(ABOUT_TEXT, reply_markup=back_kb())
    await call.answer()


@dp.callback_query(F.data == "projects")
async def cb_projects(call: types.CallbackQuery):
    await call.message.edit_text(PROJECTS_TEXT, reply_markup=back_kb())
    await call.answer()


@dp.callback_query(F.data == "contacts")
async def cb_contacts(call: types.CallbackQuery):
    await call.message.edit_text("Contacts:", reply_markup=contacts_kb())
    await call.answer()
    
# UNKNOWN MESSAGES (must stay last)

@dp.message()
async def echo(message: types.Message):
    await message.answer("I don't understand. Press /start or /menu.")


async def main():
    logging.basicConfig(level=logging.INFO)
    await set_commands(bot)
    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())