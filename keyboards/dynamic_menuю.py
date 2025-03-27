from telebot import types
from utils import load_menu_structure

def generate_dynamic_keyboard(role, section=None):
    work_docs = load_menu_structure()
    keyboard = types.InlineKeyboardMarkup()

    if role not in work_docs:
        return keyboard

    current_section = work_docs[role] if section is None else section

    for key, value in current_section.items():
        if isinstance(value, dict):
            keyboard.add(types.InlineKeyboardButton(key, callback_data=f"navigate:{key}"))
        else:
            keyboard.add(types.InlineKeyboardButton(key, url=value))

    if section is not None:
        keyboard.add(types.InlineKeyboardButton("Назад", callback_data="navigate:back"))

    return keyboard