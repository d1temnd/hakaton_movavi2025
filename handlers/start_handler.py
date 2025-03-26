from telebot import types
from data.User import User
from data.database import SessionLocal
from keyboards.main_menu import main_menu_keyboard

def start(bot, message):
    # Проверяем, есть ли пользователь в базе данных
    db = SessionLocal()
    user_id = message.from_user.id
    user = db.query(User).filter(User.telegram_id == user_id).first()

    if not user:
        bot.send_message(
            message.chat.id,
            "Добро пожаловать! Вы не зарегистрированы в системе. Выберите действие ниже:",
            reply_markup=main_menu_keyboard(user_id)
        )
    else:
        bot.send_message(
            message.chat.id,
            f"Привет, {message.from_user.first_name}! Ваша роль: {user.role}\n\nВыберите действие ниже:",
            reply_markup=main_menu_keyboard(user_id)
        )
    db.close()