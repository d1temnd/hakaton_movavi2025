import telebot
from config import Config
from data import User, Invite, SessionLocal, engine
from handlers import start, handle_inline_button

bot = telebot.TeleBot(Config.BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    start(bot, message)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    handle_inline_button(bot, call)


def db_init():
    User.metadata.create_all(bind=engine)
    Invite.metadata.create_all(bind=engine)

    db = SessionLocal()
    for admin_id in Config.ADMINS:
        admin = db.query(User).filter(User.telegram_id == admin_id).first()

        if not admin:
            new_admin = User(telegram_id=admin_id, role='admin')
            db.add(new_admin)
            db.commit()
    db.close()


if __name__ == "__main__":
    db_init()
    bot.polling(none_stop=True)