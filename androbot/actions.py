import random

from loguru import logger

from . import SessionLocal, crud, schemas
from .config import settings
from .crud import get_question, is_tg_user_already_exist
from .errors import UserExistsException, UserNotExistsException
from .models import Question
from .specialty import Specialty


def get_main_menu():
    return [e.value for e in Specialty]


def start_new_test():
    return list(map(lambda x: x.strip(), settings.answers_types.split(",")))


def add_user(tg_user: schemas.TelegramUser):
    db = SessionLocal()
    if is_tg_user_already_exist(db, tg_user.tg_user_id):
        raise UserExistsException("You try to add already exists user")
    else:
        db_user = crud.create_tg_user(db, tg_user)
        logger.info("Add new telegram user {}", tg_user)
    db.close()
    return db_user


def remove_user(tg_user: schemas.TelegramUser):
    db = SessionLocal()
    if is_tg_user_already_exist(db, tg_user.tg_user_id):
        crud.remove_answers(db, tg_user.tg_user_id)
        crud.remove_tg_user(db, tg_user.tg_user_id)
        logger.info(
            "Remove telegram user tg_user_id={}, name={}, username={}, specialty={} and answers",
            tg_user.tg_user_id,
            tg_user.name,
            tg_user.username,
            tg_user.specialty,
        )
    else:
        raise UserNotExistsException("You try to remove doesn't exist user")
    db.close()


def add_question(question: schemas.Question):
    db = SessionLocal()
    db_user = crud.add_question(db, question)
    logger.info("Add question {}", question)
    db.close()
    return db_user


def add_answer(answer: schemas.Answer):
    db = SessionLocal()
    db_user = crud.add_answer(db, answer)
    logger.info("Add new user's answer {}", answer)
    db.close()
    return db_user


def remove_questions(specialty: str):
    db = SessionLocal()
    db_user = crud.remove_questions(db, specialty)
    db.close()
    return db_user


def get_next_test(tg_user_id: int) -> Question:
    db = SessionLocal()
    tg_user = crud.get_tg_user(db, tg_user_id)
    passed_questions = crud.get_passed_questions(db, tg_user_id)
    all_question = crud.get_all_questions(db, tg_user.specialty)
    next_quest_id = random.choice(list(set(all_question) - set(passed_questions)))
    crud.set_current_question(db, tg_user_id, next_quest_id)
    next_quest = get_question(db, next_quest_id)
    db.close()
    return next_quest


def get_test_result(tg_user_id: int) -> str:
    db = SessionLocal()
    quest_id = crud.get_current_question(db, tg_user_id)
    quest = get_question(db, quest_id)
    db.close()
    return quest.text_answer
