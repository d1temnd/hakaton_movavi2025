import uuid
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from config import Config
from data import Invite, User

def get_invite_by_token(db: Session, token: str):
    return db.query(Invite).filter_by(token=token).first()

def generate_invite_token(admin_id, db, role):
    token = str(uuid.uuid4())
    expiration = datetime.now() + timedelta(days=7)
    
    # Добавляем токен в базу данных с ролью
    invite = Invite(telegram_id=admin_id, token=token, expiration=expiration, role=role)
    db.add(invite)
    db.commit()
    
    return token

def update_user_role(db: Session, user_id: int, role: str):
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if user:
        user.role = role
        db.commit()
    else:
        new_user = User(telegram_id=user_id, role=role)
        db.add(new_user)
        db.commit()

def is_admin(telegram_id):
    return telegram_id in Config.ADMINS