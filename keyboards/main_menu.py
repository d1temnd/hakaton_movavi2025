from telebot import types
from config import Config
from utils import is_admin

def main_menu_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup()

    if is_admin(user_id):
        button1 = types.InlineKeyboardButton("Проверить свою роль", callback_data="check_role")
        button2 = types.InlineKeyboardButton("Генерация инвайта", callback_data="generate_invite")
        keyboard.add(button1, button2)
    else:
        button1 = types.InlineKeyboardButton("Проверить свою роль", callback_data="check_role")
        keyboard.add(button1)

    button_docs = types.InlineKeyboardButton("Документация", callback_data="documentation")
    keyboard.add(button_docs)

    return keyboard