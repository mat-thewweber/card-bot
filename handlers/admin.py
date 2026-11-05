import html

from aiogram import F, Router, types
from aiogram.filters import Command

from config import ADMIN_ID
from repo import get_stats

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