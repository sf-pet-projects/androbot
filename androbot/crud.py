from sqlalchemy.orm import Session

from . import models, schemas
from .models import Answer, Question


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_tg_users(db: Session, skip: int = 0):
    return db.query(models.TelegramUser).offset(skip).all()


def get_tg_user(db: Session, tg_user_id: int) -> models.TelegramUser:
    return (
        db.query(models.TelegramUser).filter(models.TelegramUser.tg_user_id == tg_user_id).first()
    )


def is_tg_user_already_exist(db: Session, tg_user_id: int):
    return (
        db.query(models.TelegramUser).filter(models.TelegramUser.tg_user_id == tg_user_id).count()
        > 0
    )


def create_tg_user(db: Session, user: schemas.TelegramUser):
    db_user = models.TelegramUser(
        tg_user_id=user.tg_user_id, name=user.name, username=user.username, specialty=user.specialty
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def add_answer(db: Session, answer: schemas.Answer):
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


def add_question(db: Session, question: schemas.Question):
    db_answer = models.Question(
        question_type=question.question_type,
        text_answer=question.text_answer,
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def remove_tg_user(db: Session, tg_user_id: int):
    db.query(models.TelegramUser).filter(models.TelegramUser.tg_user_id == tg_user_id).delete()
    db.commit()


def remove_answers(db: Session, tg_user_id: int):
    db.query(Answer).filter(models.Answer.tg_user_id == tg_user_id).delete()
    db.commit()


def remove_questions(db: Session, specialty: str):
    db.query(Question).filter(models.Question.question_type == specialty).delete()
    db.commit()


def get_passed_questions(db: Session, tg_user_id: int):
    return list(
        map(
            lambda it: it.quest_id,
            db.query(models.Answer).filter(models.Answer.tg_user_id == tg_user_id).all(),
        )
    )


def set_current_question(db: Session, tg_user_id: int, quest_id: int):
    query = db.query(models.CurrentSession).filter(models.CurrentSession.tg_user_id == tg_user_id)
    if query.count() == 1:
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


def get_current_question(db: Session, tg_user_id: int):
    session = (
        db.query(models.CurrentSession)
        .filter(models.CurrentSession.tg_user_id == tg_user_id)
        .first()
    )
    return session.quest_id


def get_all_questions(db: Session, specialty: str):
    return list(
        map(
            lambda it: it.quest_id,
            db.query(models.Question).filter(models.Question.question_type == specialty).all(),
        )
    )


def get_question(db: Session, quest_id: int) -> Question:
    return db.query(models.Question).filter(models.Question.quest_id == quest_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
