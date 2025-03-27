from telebot import types
from data.User import User
from data.database import SessionLocal
from keyboards.main_menu import main_menu_keyboard
from keyboards.role_inline import role_inline_keyboard
from utils import generate_invite_token, is_admin

def handle_inline_button(bot, call):
    db = SessionLocal()
    user_id = call.from_user.id

    if call.data == "generate_invite":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "У вас нет прав для генерации инвайтов.")
            return
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите роль для нового пользователя:",
            reply_markup=role_inline_keyboard()
        )
    elif call.data == "check_role":
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if user:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"Ваша роль: {user.role}",
                reply_markup=main_menu_keyboard(user_id)
            )
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вы не зарегистрированы в системе. Пожалуйста, зарегистрируйтесь.",
                reply_markup=main_menu_keyboard(user_id)
            )
    elif call.data.startswith("role_"):
        role = call.data.split("_")[1].strip().lower()
        token = generate_invite_token(call.from_user.id, db, role)
        bot_username = bot.get_me().username
        invite_link = f"https://t.me/{bot_username}?start={token}"

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Приглашение сгенерировано для роли '{role}': {invite_link}",
            reply_markup=main_menu_keyboard(user_id)
        )
    elif call.data == "back_to_main":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите действие:",
            reply_markup=main_menu_keyboard(user_id)
        )

    db.close()