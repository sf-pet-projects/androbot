import random

from loguru import logger

from . import crud, schemas
from androbot.types.answerType import AnswerType
from .crud import get_question, is_tg_user_already_exist
from .database import SessionLocal
from .errors import NoNewQuestionsException, UserExistsException, UserNotExistsException
from .models import Question
from androbot.types.specialty import Specialty


def get_main_menu():
    return [e.value for e in Specialty]


def start_new_test():
    return [e.value for e in AnswerType]


class Actions:
    db = SessionLocal()

    def add_user(self, tg_user: schemas.TelegramUser):
        if is_tg_user_already_exist(self.db, tg_user.tg_user_id):
            raise UserExistsException("You try to add already exists user")
        else:
            db_user = crud.create_tg_user(self.db, tg_user)
            logger.info("Add new telegram user {}", tg_user)
        self.db.close()
        return db_user

    def remove_user(self, tg_user: schemas.TelegramUser):
        if is_tg_user_already_exist(self.db, tg_user.tg_user_id):
            crud.remove_sessions(self.db, tg_user.tg_user_id)
            crud.remove_answers(self.db, tg_user.tg_user_id)
            crud.remove_tg_user(self.db, tg_user.tg_user_id)
            logger.info(
                "Remove telegram user tg_user_id={}, name={}, username={}, specialty={} and answer",
                tg_user.tg_user_id,
                tg_user.name,
                tg_user.username,
                tg_user.specialty,
            )
        else:
            raise UserNotExistsException("You try to remove doesn't exist user")
        self.db.close()

    def add_question(self, question: schemas.Question):
        db_user = crud.add_question(self.db, question)
        logger.info("Add question {}", question)
        self.db.close()
        return db_user

    def add_answer(self, answer: schemas.Answer):
        db_user = crud.add_answer(self.db, answer)
        logger.info("Add new user's answer {}", answer)
        self.db.close()
        return db_user

    def remove_questions(self, specialty: str):
        db_user = crud.remove_questions(self.db, specialty)
        self.db.close()
        return db_user

    def get_next_test(self, tg_user_id: int) -> Question:
        tg_user = crud.get_tg_user(self.db, tg_user_id)
        passed_questions = crud.get_passed_questions(self.db, tg_user_id)
        all_question = crud.get_all_questions(self.db, tg_user.specialty)
        new_questions = list(set(all_question) - set(passed_questions))
        if not new_questions:
            raise NoNewQuestionsException

        next_quest_id = random.choice(new_questions)
        crud.set_current_question(self.db, tg_user_id, next_quest_id)
        next_quest = get_question(self.db, next_quest_id)
        self.db.close()
        return next_quest

    def get_test_result(self, tg_user_id: int) -> str:
        quest_id = crud.get_current_question(self.db, tg_user_id)
        quest = get_question(self.db, quest_id)
        self.db.close()
        return quest.text_answer

    def edit_specialty(self, tg_user_id: int, new_specialty: Specialty):
        if is_tg_user_already_exist(self.db, tg_user_id):
            crud.edit_specialty(self.db, tg_user_id, new_specialty)
        else:
            raise UserNotExistsException("You try to add specialty for not exist user")
        self.db.close()
