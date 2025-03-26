from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from .database import Base, SessionLocal

class Invite(Base):
    __tablename__ = 'invites'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)  # ID админа
    token = Column(String, unique=True)  # Уникальный токен
    expiration = Column(DateTime)  # Дата истечения
    role = Column(String)  # Роль для пользователя