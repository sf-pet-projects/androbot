import csv
import random
from typing import List, Optional

from loguru import logger

from . import crud, schemas
from .crud import get_question, is_tg_user_already_exist
from .database import SessionLocal
from .errors import (
    NoNewQuestionsException,
    UserExistsException,
    UserNotExistsException,
    WrongBotScoreFormat,
)
from .models import Answer, BotReview, Question, TelegramUser
from .types_ import AnswerTypes, Specialty


def get_main_menu() -> List[str]:
    return [e.value for e in Specialty]


def start_new_test() -> List[str]:
    return [e.value for e in AnswerTypes]


class Actions:
    def __init__(self) -> None:
        self.db = SessionLocal()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def add_user(self, tg_user: schemas.TelegramUser) -> TelegramUser:
        if is_tg_user_already_exist(self.db, tg_user.tg_user_id):
            raise UserExistsException("You try to add already exists user")
        else:
            db_user = crud.create_tg_user(self.db, tg_user)
            logger.info("Add new telegram user {}", tg_user)
        return db_user

    def remove_user(self, tg_user: schemas.TelegramUser) -> None:
        if is_tg_user_already_exist(self.db, tg_user.tg_user_id):
            crud.remove_events(self.db, tg_user.tg_user_id)
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

    def add_event(self, event: schemas.EventsLog) -> None:
        crud.add_event(self.db, event)
        logger.info("Add event {}", event)

    def add_question(self, question: schemas.Question) -> Question:
        db_question = crud.add_question(self.db, question)
        logger.info("Add question {}", question)
        return db_question

    def add_answer(self, answer: schemas.Answer) -> Optional[Answer]:
        has_text_answer = answer.text_answer is not None and answer.text_answer.strip()
        has_voice_answer = (
            answer.link_to_audio_answer is not None and answer.link_to_audio_answer.strip()
        )
        if has_text_answer or has_voice_answer:
            db_answer = crud.add_answer(self.db, answer)
            logger.info("Add new user's answer {}", db_answer)
            return db_answer
        return None

    def remove_questions(self, specialty: str) -> None:
        crud.remove_questions(self.db, specialty)

    def get_next_test(self, tg_user_id: int) -> Question:
        tg_user = crud.get_tg_user(self.db, tg_user_id)
        passed_questions = crud.get_passed_questions(self.db, tg_user_id)
        logger.warning(passed_questions)
        all_question = crud.get_all_questions(self.db, tg_user.specialty)
        logger.warning(all_question)
        new_questions = list(set(all_question) - set(passed_questions))
        logger.warning(new_questions)
        if not new_questions:
            crud.remove_sessions(self.db, tg_user.tg_user_id)
            raise NoNewQuestionsException("All questions were answered")

        next_quest_id = random.choice(new_questions)
        crud.set_current_question(self.db, tg_user_id, next_quest_id)
        next_quest = get_question(self.db, next_quest_id)
        return next_quest

    def has_started_test(self, tg_user_id: int) -> bool:
        return crud.get_current_question(self.db, tg_user_id) is not None

    def get_current_question(self, tg_user_id: int) -> Optional[Question]:
        quest_id = crud.get_current_question(self.db, tg_user_id)
        if quest_id is not None:
            quest = get_question(self.db, quest_id)
            return quest
        else:
            return None

    def edit_specialty(self, tg_user_id: int, new_specialty: Specialty) -> None:
        if is_tg_user_already_exist(self.db, tg_user_id):
            crud.edit_specialty(self.db, tg_user_id, new_specialty)
        else:
            raise UserNotExistsException("You try to add specialty for not exist user")

    def load_questions(self, specialty: Specialty, file: str) -> None:
        with open(file, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    continue
                self.add_question(
                    Question(
                        question_type=specialty.value,
                        question_category=row[0],
                        text_question=row[1],
                        text_answer=row[2],
                        additional_info=row[3],
                    )
                )

    def reset_session(self, user: schemas.TelegramUser) -> None:
        crud.remove_answers(self.db, user.tg_user_id)
        crud.remove_sessions(self.db, user.tg_user_id)

    def add_bot_score(self, user: schemas.TelegramUser, bot_score: int) -> BotReview:
        if bot_score not in range(1, 10):
            raise WrongBotScoreFormat(
                "You can have only 1 to 10 score in field BotReview.bot_score"
            )
        return crud.add_bot_score(self.db, user.tg_user_id, bot_score)

    def get_bot_review(self, user: schemas.TelegramUser) -> BotReview:
        return crud.get_bot_review(self.db, user.tg_user_id)
