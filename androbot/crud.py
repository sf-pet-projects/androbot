from typing import List, Optional

from sqlalchemy.orm import Session

from androbot.database import Base

from . import models, schemas
from .errors import NoCurrentSessionException
from .models import (
    AdditionalInfo,
    Answer,
    BotReview,
    CurrentSession,
    EventsLog,
    ProblemQuestionReview,
    Question,
    QuestionScore,
    TelegramUser,
)
from .types_ import Specialty


def get_tg_users(db: Session, skip: int = 0) -> List[TelegramUser]:
    """
    Получить список пользователей
    """
    return db.query(models.TelegramUser).offset(skip).all()


def get_tg_user(db: Session, tg_user_id: int) -> TelegramUser:
    """
    Получить пользователя по tg_user_id
    """
    return db.query(models.TelegramUser).filter(models.TelegramUser.tg_user_id == tg_user_id).first()


def is_tg_user_already_exist(db: Session, tg_user_id: int) -> bool:
    """
    Проверяем есть ли уже в базе пользователь с таким tg_user_id
    """
    return db.query(TelegramUser).filter(TelegramUser.tg_user_id == tg_user_id).count() > 0


def create_tg_user(db: Session, user: schemas.TelegramUser) -> TelegramUser:
    """
    Создаем пользователя в базе
    """
    db_user = models.TelegramUser(
        tg_user_id=user.tg_user_id, name=user.name, username=user.username, specialty=user.specialty
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def add_event(db: Session, event: schemas.EventsLog) -> EventsLog:
    """
    Сохранение события
    """
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
    """
    Добавление ответа пользователя на вопрос в базу
    """

    current_session = get_current_session(db, answer.tg_user_id)

    if not current_session:
        raise NoCurrentSessionException

    db_answer = models.Answer(
        quest_id=answer.quest_id,
        tg_user_id=answer.tg_user_id,
        answer_type=answer.answer_type,
        text_answer=answer.text_answer,
        link_to_audio_answer=answer.link_to_audio_answer,
        session_id=current_session.id,
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def add_question(db: Session, question: schemas.Question) -> Question:
    """
    Добавление вопроса в базу
    """
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


def get_passed_questions(db: Session, tg_user_id: int) -> List[int]:
    """
    Получить список id вопросов, на которые ответил пользователь tg_user_id
    """

    current_session = get_current_session(db, tg_user_id)
    if current_session:
        session_id = current_session.id
    else:
        session_id = None

    return (
        db.query(models.Answer.quest_id)
        .filter((models.Answer.tg_user_id == tg_user_id) & (models.Answer.session_id == session_id))
        .all()
    )


def set_current_question(db: Session, tg_user_id: int, quest_id: int) -> Session:
    """
    Назначить вопрос quest_id пользователю tg_user_id
    """
    query = db.query(models.CurrentSession).filter(
        (models.CurrentSession.tg_user_id == tg_user_id) & (models.CurrentSession.is_finished == False)  # noqa E712
    )
    if query is not None and query.count() == 1:
        db_session = query.first()
        db_session.quest_id = quest_id
    else:
        db_session = models.CurrentSession(
            quest_id=quest_id,
            tg_user_id=tg_user_id,
            is_finished=False,
        )
        db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def edit_specialty(db: Session, tg_user_id: int, specialty: Specialty) -> None:
    """
    Редактируем специальность у пользователя
    """
    query = db.query(models.TelegramUser).filter(models.TelegramUser.tg_user_id == tg_user_id)
    if query is not None and query.count() == 1:
        db_session = query.first()
        db_session.specialty = specialty.value
        db.commit()
        db.refresh(db_session)
    db.close()


def get_current_session(db: Session, tg_user_id: int) -> Optional[CurrentSession]:
    """
    Получаем текущую сессию пользователя tg_user_id
    """
    return (
        db.query(CurrentSession)
        .filter((CurrentSession.tg_user_id == tg_user_id) & (CurrentSession.is_finished == False))  # noqa E712
        .first()
    )


def get_current_question(db: Session, tg_user_id: int) -> Optional[int]:
    """
    Получаем текущий вопрос пользователя tg_user_id
    """
    session = get_current_session(db, tg_user_id)
    if session is not None and session.quest_id != 0:
        return session.quest_id
    else:
        return None


def add_train_material(db: Session, question_id: int, tg_user_id: int) -> None:
    """
    Добавляем в базу данных тренировочные материалы по вопросу question_id для пользователя tg_user_id
    """
    additional_info = models.AdditionalInfo(tg_user_id=tg_user_id, question_id=question_id)
    commit_into_db(db, additional_info)


def get_all_questions(db: Session, specialty: str) -> List[Question]:
    """
    Получаем список всех вопросов для специальности specialty
    """
    return db.query(models.Question.id).filter(models.Question.question_type == specialty).all()


def get_question(db: Session, quest_id: int) -> Question:
    """
    Получаем вопрос по question_id
    """
    return db.query(Question).filter(models.Question.id == quest_id).first()


def get_train_material(db: Session, tg_user_id: int) -> List[AdditionalInfo]:
    """
    Получаем тренировочные материалы для пользователя tg_user_id
    """
    return list(db.query(AdditionalInfo).filter(models.AdditionalInfo.tg_user_id == tg_user_id))


def add_bot_score(db: Session, tg_user_id: int, bot_score: int) -> BotReview:
    """
    Добавить оценку бота от пользователя tg_user_id
    """
    db_review = db.query(BotReview).filter(models.BotReview.tg_user_id == tg_user_id).first()
    if db_review is not None:
        db_review.bot_score = bot_score
        commit_into_db(db, db_review)
        return db_review
    else:
        bot_review = models.BotReview(tg_user_id=tg_user_id, bot_score=bot_score, bot_review=None, bot_review_type=None)
        commit_into_db(db, bot_review)
        return bot_review


def add_bot_review(db: Session, tg_user_id: int, review: str, review_type: str) -> BotReview:
    """
    Добавить ревью на бота от пользователя tg_user_id
    """
    db_review = db.query(BotReview).filter(models.BotReview.tg_user_id == tg_user_id).first()
    if db_review is not None:
        bot_review = models.BotReview(
            tg_user_id=tg_user_id, bot_score=db_review.bot_score, bot_review=review, bot_review_type=review_type
        )
        commit_into_db(db, bot_review)
        return db_review
    else:
        bot_review = models.BotReview(
            tg_user_id=tg_user_id, bot_score=None, bot_review=review, bot_review_type=review_type
        )
        commit_into_db(db, bot_review)
        return bot_review


def add_question_score(db: Session, question_id: int, tg_user_id: int, score: int) -> QuestionScore:
    """
    Добавить оценку вопроса
    """
    db_question_score = models.QuestionScore(question_id=question_id, tg_user_id=tg_user_id, score=score)
    commit_into_db(db, db_question_score)
    return db_question_score


def get_questions_scores(db: Session, tg_user_id: int) -> List[QuestionScore]:
    """
    Получаем все оценки вопросов от пользователя tg_user_id
    """
    db_question_score = db.query(QuestionScore).filter(models.QuestionScore.tg_user_id == tg_user_id)
    return list(db_question_score)


def get_question_score(db: Session, question_id: int, tg_user_id: int) -> QuestionScore:
    """
    Получаем оценку вопроса question_id от пользователя tg_user_id
    """
    db_question_score = db.query(QuestionScore).filter(
        models.QuestionScore.tg_user_id == tg_user_id and models.QuestionScore.question_id == question_id
    )
    return db_question_score


def get_bot_review(db: Session, tg_user_id: int) -> List[BotReview]:
    """
    Получаем ревью на бот пользователя tg_user_id
    """
    db_review = db.query(BotReview).filter(models.BotReview.tg_user_id == tg_user_id)
    return db_review


def get_problem_question_review(db: Session, tg_user_id: int) -> List[ProblemQuestionReview]:
    """
    Получаем список оставленных ревью на вопросы от пользователя tg_user_id
    """
    db_problems = db.query(ProblemQuestionReview).filter(models.ProblemQuestionReview.tg_user_id == tg_user_id)
    return db_problems


def add_problem_question_review(
    db: Session, question_id: int, tg_user_id: int, review: str, review_type: str
) -> ProblemQuestionReview:
    """
    Добавляем в базу данных ревью от пользователя tg_user_id по вопросу question_id
    """
    db_problem = models.ProblemQuestionReview(
        question_id=question_id, tg_user_id=tg_user_id, review=review, review_type=review_type
    )
    commit_into_db(db, db_problem)
    return db_problem


def commit_into_db(db: Session, data: Base):
    """
    Коммит записи в базу и закрытие сессии
    """
    db.add(data)
    db.commit()
    db.refresh(data)
    db.close()


def remove_tg_user(db: Session, tg_user_id: int) -> None:
    """
    Удаляем пользователя из базы по tg_user_id
    """
    db.query(models.TelegramUser).filter(models.TelegramUser.tg_user_id == tg_user_id).delete()
    db.commit()


def remove_answers(db: Session, tg_user_id: int) -> None:
    """
    Удаляем ответы пользователя на вопросы по tg_user_id
    """
    db.query(Answer).filter(models.Answer.tg_user_id == tg_user_id).delete()
    db.commit()


def remove_sessions(db: Session, tg_user_id: int) -> None:
    """
    Удаляем сессию пользователя по tg_user_id
    """
    current_session = get_current_session(db, tg_user_id)
    if not current_session:
        raise NoCurrentSessionException

    current_session.is_finished = True
    db.add(current_session)
    db.commit()


def remove_events(db: Session, tg_user_id: int) -> None:
    """
    Удаляем события пользователя по tg_user_id
    """
    db.query(EventsLog).filter(models.EventsLog.tg_user_id == tg_user_id).delete()
    db.commit()


def remove_questions(db: Session, specialty: str) -> None:
    """
    Удаляем вопросы по категории (specialty)
    """
    db.query(Question).filter(models.Question.question_type == specialty).delete()
    db.commit()


def remove_problem_question_review(db: Session, tg_user_id: int, question_id: int) -> None:
    """
    Удаляем замечания пользователя c tg_user_id по вопросy question_id
    """
    db.query(ProblemQuestionReview).filter(
        models.ProblemQuestionReview.tg_user_id == tg_user_id
        and models.ProblemQuestionReview.question_id == question_id
    ).delete()
    db.commit()


def remove_question_score(db: Session, question_id: int) -> None:
    """
    Удаляем оценку вопроса с question_id
    """
    db.query(QuestionScore).filter(models.QuestionScore.question_id == question_id).delete()
    db.commit()


def remove_train_material(db: Session, tg_user_id: int, question_id: int) -> None:
    """
    Удаляем тренировочные материалы по вопросу question_id для пользователя c tg_user_id
    """
    db.query(AdditionalInfo).filter(
        models.AdditionalInfo.tg_user_id == tg_user_id and models.AdditionalInfo.question_id == question_id
    ).delete()
    db.commit()


def remove_train_materials(db: Session, tg_user_id: int) -> None:
    """
    Удаляем тренировочные материалы для пользователя c tg_user_id
    """
    db.query(AdditionalInfo).filter(models.AdditionalInfo.tg_user_id == tg_user_id).delete()
    db.commit()
