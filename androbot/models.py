import datetime as datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class TelegramUser(Base):
    __tablename__ = "tg_users"

    tg_user_id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, unique=False, index=True)
    username = Column(String, unique=True, index=True)
    specialty = Column(String, unique=False, index=True)
    session = relationship("CurrentSession")
    events = relationship("EventsLog")


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    quest_id = Column(Integer, ForeignKey("question.id"))
    session_id = Column(Integer, ForeignKey("session.id"))
    tg_user_id = Column(Integer, primary_key=False, unique=False, index=True)
    answer_type = Column(String, unique=False, index=True)
    text_answer = Column(String, unique=False, index=False)
    link_to_audio_answer = Column(String, unique=False, index=False)


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    question_type = Column(String, unique=False, index=True)
    question_category = Column(String, unique=False, index=False)
    text_question = Column(String, unique=False, index=False)
    text_answer = Column(String, unique=False, index=False)
    additional_info = Column(String, unique=False, index=False)
    question = relationship("Answer")


class CurrentSession(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    tg_user_id = Column(Integer, ForeignKey("tg_users.tg_user_id"))
    quest_id = Column(Integer, ForeignKey("question.id"))
    is_finished = Column(Boolean, unique=False, index=False, default=False)


class EventsLog(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    tg_user_id = Column(Integer, ForeignKey("tg_users.tg_user_id"))
    event_type = Column(String, unique=False, index=True)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
    param1 = Column(String, unique=False, index=True)
    param2 = Column(String, unique=False, index=True)
    param3 = Column(String, unique=False, index=True)
    param4 = Column(String, unique=False, index=True)
    param5 = Column(String, unique=False, index=True)


class BotReview(Base):
    __tablename__ = "bot_review"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    tg_user_id = Column(Integer, ForeignKey("tg_users.tg_user_id"))
    bot_score = Column(Integer, unique=False, index=True, nullable=True)
    bot_review = Column(String, unique=False, index=True, nullable=True)
    bot_review_type = Column(String, unique=False, index=True, nullable=True)


class QuestionScore(Base):
    __tablename__ = "question_score"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    tg_user_id = Column(Integer, ForeignKey("tg_users.tg_user_id"))
    question_id = Column(Integer, ForeignKey("question.id"))
    score = Column(Integer, unique=False, index=True)


class ProblemQuestionReview(Base):
    __tablename__ = "problem_question_review"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    tg_user_id = Column(Integer, ForeignKey("tg_users.tg_user_id"))
    review = Column(String, unique=False, index=True)
    review_type = Column(String, unique=False, index=True)


class AdditionalInfo(Base):
    __tablename__ = "additional_info"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    tg_user_id = Column(Integer, ForeignKey("tg_users.tg_user_id"))
