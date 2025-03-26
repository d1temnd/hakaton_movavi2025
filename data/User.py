from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .database import Base, SessionLocal

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, index=True)
    role = Column(String)