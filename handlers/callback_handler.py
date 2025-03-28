import telebot
from telebot import types
from telebot.types import *
from data.User import User
from data.database import SessionLocal
from keyboards.main_menu import main_menu_keyboard
from keyboards.role_inline import role_inline_keyboard
from utils import generate_invite_token, is_admin, load_work_docs

def handle_inline_button(bot, call):
    db = SessionLocal()
    user_id = call.from_user.id

    if call.data == "documentation":
        user = db.query(User).filter(User.telegram_id == user_id).first()
        docs = load_work_docs()

        if is_admin(user_id):
            send_menu(bot, call.message.chat.id, docs, "", call.message.message_id)
        elif user:
            role_docs = docs.get(user.role, {})
            send_menu(bot, call.message.chat.id, role_docs, "", call.message.message_id)
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Вы не зарегистрированы в системе. Пожалуйста, зарегистрируйтесь.",
                reply_markup=main_menu_keyboard(user_id)
            )
            db.close()
            return

    elif call.data.startswith("menu_"):
        path = call.data[5:]

        if path == "root":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Выберите действие:",
                reply_markup=main_menu_keyboard(user_id)
            )
            db.close()
            return

        docs = load_work_docs()

        if is_admin(user_id):
            menu = docs
        else:
            user = db.query(User).filter(User.telegram_id == user_id).first()
            menu = docs.get(user.role, {})
        try:
            for key in path.split("/"):
                if key: 
                    menu = menu[key]
        except KeyError:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Ошибка навигации! Попробуйте снова.",
                reply_markup=main_menu_keyboard(user_id)
            )
            db.close()
            return

        send_menu(bot, call.message.chat.id, menu, path, call.message.message_id)

    elif call.data == "generate_invite":
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "У вас нет прав для генерации инвайтов.")
            return
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите роль для нового пользователя:",
            reply_markup=role_inline_keyboard()
        )

    elif call.data.startswith("role_"):
        role = call.data.split("_")[1].strip().lower()
        token = generate_invite_token(call.from_user.id, db, role)
        bot_username = bot.get_me().username
        invite_link = f"https://t.me/{bot_username}?start={token}"

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("❌ Скрыть", callback_data="hide_message"))

        bot.send_message(
            chat_id=call.message.chat.id,
            text=f"Приглашение сгенерировано для роли '{role}': {invite_link}",
            reply_markup=markup
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

    elif call.data == "back_to_main":
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Выберите действие:",
                reply_markup=main_menu_keyboard(user_id)
            )
        except telebot.apihelper.ApiTelegramException as e:
                print("Сообщение не изменено, игнорируем ошибку.")
    
    elif call.data == "hide_message":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    db.close()


def send_menu(bot, chat_id, menu, path="", message_id=None):
    markup = InlineKeyboardMarkup()

    for key, value in menu.items():
        new_path = f"{path}/{key}" if path else key
        if isinstance(value, str):  # Это конечная точка
            if value.startswith("http://") or value.startswith("https://"):
                markup.add(InlineKeyboardButton(key, url=value))
            else:
                print(f"Некорректный URL: {value}")
        else:
            markup.add(InlineKeyboardButton(key, callback_data=f"menu_{new_path}"))

    
    if path:
        parent_path = "/".join(path.split("/")[:-1])
        markup.add(InlineKeyboardButton("🔙 Назад", callback_data=f"menu_{parent_path}" if parent_path else "documentation"))
    markup.add(InlineKeyboardButton("🏠 Главное меню", callback_data="menu_root"))

    if message_id:
        try:
            bot.edit_message_text(
                "Выберите раздел:",
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=markup
            )
        except telebot.apihelper.ApiTelegramException as e:
            print("Сообщение не изменено, игнорируем ошибку.")
    else:
        bot.send_message(chat_id, "Выберите раздел:", reply_markup=markup)