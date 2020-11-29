from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class TelegramUser(Base):
    __tablename__ = "tg_users"

    tg_user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=True)
    username = Column(String, unique=True, index=True)
    specialty = Column(String, unique=False, index=True)


class Answer(Base):
    __tablename__ = "answer"

    answer_id = Column(Integer, primary_key=True, index=True)
    quest_id = Column(Integer, primary_key=False, index=True)
    tg_user_id = Column(Integer, primary_key=False, unique=False, index=True)
    answer_type = Column(String, unique=False, index=True)
    text_answer = Column(String, unique=False, index=True)
    link_to_audio_answer = Column(String, unique=False, index=True)


class Question(Base):
    __tablename__ = "question"

    quest_id = Column(Integer, primary_key=True, index=True)
    question_type = Column(String, unique=False, index=True)
    text_answer = Column(String, unique=False, index=True)
