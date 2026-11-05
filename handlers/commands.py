from aiogram import Router, types
from aiogram.filters import Command
from repo import get_projects, add_user
from repo import add_user
from keyboards import back_kb, contacts_kb, main_menu_kb
from texts import (
    ABOUT_TEXT,
    CONTACTS_TEXT,
    HELP_TEXT,
    MENU_TEXT,
    PROJECTS_TEXT,
    UNKNOWN_TEXT,
    format_projects,
)

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user = message.from_user
    await add_user(user.id, user.username, user.full_name)
    await message.answer(
        f"Hello, {user.full_name}!\n{MENU_TEXT}",
        reply_markup=main_menu_kb(),
    )

@router.message(Command("menu"))
async def cmd_menu(message: types.Message):
    await message.answer(MENU_TEXT, reply_markup=main_menu_kb())

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(HELP_TEXT)

@router.message(Command("about"))
async def cmd_about(message: types.Message):
    await message.answer(ABOUT_TEXT, reply_markup=back_kb())

@router.message(Command("projects"))
async def cmd_projects(message: types.Message):
    projects = await get_projects()
    await message.answer(format_projects(projects), reply_markup=back_kb())

@router.message(Command("contacts"))
async def cmd_contacts(message: types.Message):
    await message.answer(CONTACTS_TEXT, reply_markup=contacts_kb())

# Должен быть последним в файле
@router.message()
async def unknown(message: types.Message):
    await message.answer(UNKNOWN_TEXT)