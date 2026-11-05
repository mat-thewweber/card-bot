import html
import re

from aiogram import Bot, F, Router, types
from aiogram.exceptions import TelegramForbiddenError
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import ADMIN_ID
from keyboards import cancel_kb, main_menu_kb
from texts import FEEDBACK_ASK, FEEDBACK_SENT, FEEDBACK_TEXT_ONLY, MENU_TEXT

router = Router()


class Feedback(StatesGroup):
    waiting_text = State()


@router.callback_query(F.data == "feedback")
async def start_feedback(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Feedback.waiting_text)
    await call.message.edit_text(FEEDBACK_ASK, reply_markup=cancel_kb())
    await call.answer()


@router.callback_query(F.data == "cancel")
async def cancel_feedback(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(MENU_TEXT, reply_markup=main_menu_kb())
    await call.answer()


@router.message(Feedback.waiting_text, F.text.startswith("/"))
async def command_while_waiting(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Cancelled. Send the command again.", reply_markup=main_menu_kb())


@router.message(Feedback.waiting_text, F.text)
async def receive_feedback(message: types.Message, state: FSMContext, bot: Bot):
    user = message.from_user
    username = f"@{user.username}" if user.username else "no username"
    await bot.send_message(
        ADMIN_ID,
        f"<b>New message</b>\n"
        f"From: {html.escape(user.full_name)} ({html.escape(username)})\n"
        f"ID: <code>{user.id}</code>\n\n"
        f"{html.escape(message.text)}",
    )
    await state.clear()
    await message.answer(FEEDBACK_SENT, reply_markup=main_menu_kb())


@router.message(Feedback.waiting_text)
async def not_text(message: types.Message):
    await message.answer(FEEDBACK_TEXT_ONLY, reply_markup=cancel_kb())


@router.message(F.from_user.id == ADMIN_ID, F.reply_to_message, F.text)
async def admin_reply(message: types.Message, bot: Bot):
    source = message.reply_to_message.text or ""
    match = re.search(r"ID: (\d+)", source)
    if match is None:
        await message.answer("I can't find a user ID in that message.")
        return
    try:
        await bot.send_message(
            int(match.group(1)),
            f"<b>Reply from Matthew:</b>\n\n{html.escape(message.text)}",
        )
    except TelegramForbiddenError:
        await message.answer("The user has blocked the bot.")
        return
    await message.answer("Sent.")