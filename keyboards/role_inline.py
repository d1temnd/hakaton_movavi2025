from telebot import types

def role_inline_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Куратор", callback_data="role_curator")
    button2 = types.InlineKeyboardButton("Преподаватель", callback_data="role_teacher")
    button_back = types.InlineKeyboardButton("Назад", callback_data="back_to_main")
    keyboard.add(button1, button2)
    keyboard.add(button_back)
    return keyboard