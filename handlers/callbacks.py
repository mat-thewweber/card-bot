from aiogram import F, Router, types

from keyboards import back_kb, contacts_kb, main_menu_kb
from texts import ABOUT_TEXT, CONTACTS_TEXT, MENU_TEXT, PROJECTS_TEXT

router = Router()

@router.callback_query(F.data == "menu")
async def cb_menu(call: types.CallbackQuery):
    await call.message.edit_text(MENU_TEXT, reply_markup=main_menu_kb())
    await call.answer()

@router.callback_query(F.data == "about")
async def cb_about(call: types.CallbackQuery):
    await call.message.edit_text(ABOUT_TEXT, reply_markup=back_kb())
    await call.answer()

@router.callback_query(F.data == "projects")
async def cb_projects(call: types.CallbackQuery):
    await call.message.edit_text(PROJECTS_TEXT, reply_markup=back_kb())
    await call.answer()

@router.callback_query(F.data == "contacts")
async def cb_contacts(call: types.CallbackQuery):
    await call.message.edit_text(CONTACTS_TEXT, reply_markup=contacts_kb())
    await call.answer()