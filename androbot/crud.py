from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas
from .models import Answer, BotReview, CurrentSession, EventsLog, Question, TelegramUser
from .types_ import Specialty


def get_tg_users(db: Session, skip: int = 0) -> List[TelegramUser]:
    return db.query(models.TelegramUser).offset(skip).all()


def get_tg_user(db: Session, tg_user_id: int) -> TelegramUser:
    return (
        db.query(models.TelegramUser).filter(models.TelegramUser.tg_user_id == tg_user_id).first()
    )


def is_tg_user_already_exist(db: Session, tg_user_id: int) -> bool:
    return db.query(TelegramUser).filter(TelegramUser.tg_user_id == tg_user_id).count() > 0


def create_tg_user(db: Session, user: schemas.TelegramUser) -> TelegramUser:
    db_user = models.TelegramUser(
        tg_user_id=user.tg_user_id, name=user.name, username=user.username, specialty=user.specialty
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def add_event(db: Session, event: schemas.EventsLog) -> EventsLog:
    db_event = models.EventsLog(
        tg_user_id=event.tg_user_id,
        event_type=event.event_type.value,
        datetime=event.datetime,
        param1=event.param1,
        param2=event.param2,
        param3=event.param3,
        param4=event.param4,
        param5=event.param5,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def add_answer(db: Session, answer: schemas.Answer) -> Answer:
    db_answer = models.Answer(
        quest_id=answer.quest_id,
        tg_user_id=answer.tg_user_id,
        answer_type=answer.answer_type,
        text_answer=answer.text_answer,
        link_to_audio_answer=answer.link_to_audio_answer,
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def add_question(db: Session, question: schemas.Question) -> Question:
    db_question = models.Question(
        question_type=question.question_type,
        question_category=question.question_category,
        text_answer=question.text_answer,
        text_question=question.text_question,
        additional_info=question.additional_info,
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    question.id = db_question.id
    return db_question


def remove_tg_user(db: Session, tg_user_id: int) -> None:
    db.query(models.TelegramUser).filter(models.TelegramUser.tg_user_id == tg_user_id).delete()
    db.commit()


def remove_answers(db: Session, tg_user_id: int) -> None:
    db.query(Answer).filter(models.Answer.tg_user_id == tg_user_id).delete()
    db.commit()


def remove_sessions(db: Session, tg_user_id: int) -> None:
    db.query(CurrentSession).filter(models.CurrentSession.tg_user_id == tg_user_id).delete()
    db.commit()


def remove_events(db: Session, tg_user_id: int) -> None:
    db.query(EventsLog).filter(models.EventsLog.tg_user_id == tg_user_id).delete()
    db.commit()


def remove_questions(db: Session, specialty: str) -> None:
    db.query(Question).filter(models.Question.question_type == specialty).delete()
    db.commit()


def get_passed_questions(db: Session, tg_user_id: int) -> List[int]:
    return db.query(models.Answer.quest_id).filter(models.Answer.tg_user_id == tg_user_id).all()


def set_current_question(db: Session, tg_user_id: int, quest_id: int) -> Session:
    query = db.query(models.CurrentSession).filter(models.CurrentSession.tg_user_id == tg_user_id)
    if query is not None and query.count() == 1:
        db_session = query.first()
        db_session.quest_id = quest_id
    else:
        db_session = models.CurrentSession(
            quest_id=quest_id,
            tg_user_id=tg_user_id,
        )
        db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def edit_specialty(db: Session, tg_user_id: int, specialty: Specialty) -> None:
    query = db.query(models.TelegramUser).filter(models.TelegramUser.tg_user_id == tg_user_id)
    if query is not None and query.count() == 1:
        db_session = query.first()
        db_session.specialty = specialty.value
        db.commit()
        db.refresh(db_session)
    db.close()


def get_current_question(db: Session, tg_user_id: int) -> Optional[int]:
    session = db.query(CurrentSession).filter(CurrentSession.tg_user_id == tg_user_id).first()
    if session is not None and session.quest_id != 0:
        return session.quest_id
    else:
        return None


def get_all_questions(db: Session, specialty: str) -> List[Question]:
    return db.query(models.Question.id).filter(models.Question.question_type == specialty).all()


def get_question(db: Session, quest_id: int) -> Question:
    return db.query(Question).filter(models.Question.id == quest_id).first()


def add_bot_score(db: Session, tg_user_id: int, bot_score: int) -> BotReview:
    db_review = db.query(BotReview).filter(models.BotReview.tg_user_id == tg_user_id).first()
    if db_review is not None:
        db_review.bot_score = bot_score
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        db.close()
        return db_review
    else:
        bot_review = models.BotReview(tg_user_id=tg_user_id, bot_score=bot_score)
        db.add(bot_review)
        db.commit()
        db.refresh(bot_review)
        db.close()
        return bot_review


def get_bot_review(db: Session, tg_user_id: int) -> BotReview:
    db_review = db.query(BotReview).filter(models.BotReview.tg_user_id == tg_user_id).first()
    return db_review
