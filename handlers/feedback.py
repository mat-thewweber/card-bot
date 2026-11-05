from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import cancel_kb, main_menu_kb
from texts import FEEDBACK_ASK, MENU_TEXT

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