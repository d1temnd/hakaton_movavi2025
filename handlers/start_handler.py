from telebot import types
from data.User import User
from data.database import SessionLocal
from keyboards.main_menu import main_menu_keyboard
from utils import get_invite_by_token

def start(bot, message):
    db = SessionLocal()
    user_id = message.from_user.id
    args = message.text.split()  # Получаем аргументы (токен инвайта, если есть)

    user = db.query(User).filter(User.telegram_id == user_id).first()

    if not user:
        if len(args) > 1:
            token = args[1]
            invite = get_invite_by_token(token, db)
            if invite:
                new_user = User(telegram_id=user_id, role=invite.role)
                db.add(new_user)
                db.commit()
                db.delete(invite)
                db.commit()
                bot.send_message(
                    message.chat.id,
                    f"Вы успешно зарегистрированы как {invite.role}!",
                    reply_markup=main_menu_keyboard(user_id)
                )
            else:
                bot.send_message(message.chat.id, "Неверный или устаревший инвайт!")
        else:
            bot.send_message(message.chat.id, "Вы не зарегистрированы. Запросите инвайт у администратора.")
    else:
        bot.send_message(
            message.chat.id,
            f"Привет, {message.from_user.first_name}! Ваша роль: {user.role}",
            reply_markup=main_menu_keyboard(user_id)
        )

    db.close()