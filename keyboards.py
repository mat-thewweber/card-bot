from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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