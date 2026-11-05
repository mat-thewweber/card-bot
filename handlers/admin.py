import html

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import ADMIN_ID
from repo import add_project, get_stats

router = Router()
router.message.filter(F.from_user.id == ADMIN_ID)


@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    stats = await get_stats()
    lines = [
        "<b>Stats</b>",
        f"Users: {stats['total']}",
        f"New in 7 days: {stats['week']}",
        f"Projects: {stats['projects']}",
        "",
        "<b>Last users</b>",
    ]
    for i, user in enumerate(stats["last"], 1):
        username = f"@{user.username}" if user.username else "no username"
        lines.append(f"{i}. {html.escape(user.full_name)} ({html.escape(username)})")
    await message.answer("\n".join(lines))

class AddProject(StatesGroup):
    title = State()
    description = State()
    url = State()


@router.message(Command("add_project"))
async def cmd_add_project(message: types.Message, state: FSMContext):
    await state.set_state(AddProject.title)
    await message.answer("Project title? Send /cancel to stop.")


@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Cancelled.")


@router.message(AddProject.title, F.text, ~F.text.startswith("/"))
async def get_title(message: types.Message, state: FSMContext):
    title = message.text.strip()
    if len(title) > 100:
        await message.answer("Title is too long, max 100 characters. Try again.")
        return
    await state.update_data(title=title)
    await state.set_state(AddProject.description)
    await message.answer("Short description?")


@router.message(AddProject.description, F.text, ~F.text.startswith("/"))
async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text.strip())
    await state.set_state(AddProject.url)
    await message.answer("Link (for example GitHub)? Send - to skip.")


@router.message(AddProject.url, F.text, ~F.text.startswith("/"))
async def get_url(message: types.Message, state: FSMContext):
    text = message.text.strip()
    url = None if text == "-" else text
    if url and not url.startswith(("http://", "https://")):
        await message.answer("The link must start with http:// or https://. Or send -")
        return
    data = await state.get_data()
    await state.clear()
    await add_project(data["title"], data["description"], url)
    await message.answer("Project added. Check it in /projects")