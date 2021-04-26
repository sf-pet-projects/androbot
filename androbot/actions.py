import csv
import random
from typing import List, Optional

from loguru import logger

from . import crud, schemas
from .crud import get_question, is_tg_user_already_exist
from .database import SessionLocal
from .errors import NoNewQuestionsException, UserExistsException, UserNotExistsException, WrongBotScoreFormat
from .models import (
    AdditionalInfo,
    Answer,
    BotReview,
    CurrentSession,
    ProblemQuestionReview,
    Question,
    QuestionScore,
    TelegramUser,
)
from .types_ import AnswerTypes, Specialty


def get_main_menu() -> List[str]:
    """
    Получаем список доступных специальностей
    """
    return [e.value for e in Specialty]


def start_new_test() -> List[str]:
    """
    Получаем список доступных способов для ответа
    """
    return [e.value for e in AnswerTypes]


class Actions:
    def __init__(self) -> None:
        self.db = SessionLocal()

    def __enter__(self):
        return self

    def __close__(self):
        self.db.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def add_user(self, tg_user: schemas.TelegramUser) -> TelegramUser:
        """
        Добавляем пользователя в базу данных
        """
        if is_tg_user_already_exist(self.db, tg_user.tg_user_id):
            raise UserExistsException("You try to add already exists user")
        else:
            db_user = crud.create_tg_user(self.db, tg_user)
            logger.info("Add new telegram user {}", tg_user)
        return db_user

    def remove_user(self, tg_user: schemas.TelegramUser) -> None:
        """
        Удаляем информацию о пользователе из баз по tg_user_id [CurrentSession, EventsLog, Answer, TelegramUser]
        """
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
        """
        Добавляем в базу данных событие
        """
        crud.add_event(self.db, event)
        logger.info("Add event {}", event)

    def add_question(self, question: schemas.Question) -> Question:
        """
        Добавляем в базу данных вопрос
        """
        db_question = crud.add_question(self.db, question)
        logger.info("Add question {}", question)
        return db_question

    def add_answer(self, answer: schemas.Answer) -> Optional[Answer]:
        """
        Добавляем в базу данных ответ пользователя на вопрос
        """
        has_text_answer = answer.text_answer is not None and answer.text_answer.strip()
        has_voice_answer = answer.link_to_audio_answer is not None and answer.link_to_audio_answer.strip()
        if has_text_answer or has_voice_answer:
            db_answer = crud.add_answer(self.db, answer)
            logger.info("Add new user's answer {}", db_answer)
            return db_answer
        return None

    def get_next_test(self, tg_user_id: int) -> Question:
        """
        Получить из базы данных следующий тест для пользователя tg_user_id
        """
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

    def get_current_session(self, tg_user_id: int) -> Optional[CurrentSession]:
        """
        Получить из базы данных текущую сессию пользователя
        """
        return crud.get_current_session(self.db, tg_user_id)

    def has_started_test(self, tg_user_id: int) -> bool:
        """
        Проверка, есть ли у пользователя tg_user_id начатый тест (текущий вопрос не None)
        """
        return crud.get_current_question(self.db, tg_user_id) is not None

    def add_train_material(self, question_id: int, tg_user_id: int) -> None:
        """
        Добавить в базу данных признак того,
        что пользователь c tg_user_id запросил дополнительный материал по вопросу question_id
        """
        return crud.add_train_material(self.db, question_id, tg_user_id)

    def get_train_material(self, tg_user_id: int) -> List[AdditionalInfo]:
        """
        Получить из базы данных список вопросов по которым пользователь tg_user_id запросил дополнительный материал
        """
        return crud.get_train_material(self.db, tg_user_id)

    def get_current_question(self, tg_user_id: int) -> Optional[Question]:
        """
        Получить из базы данных текущий вопрос для пользователя (случайный вопрос из тех, на которые нет ответа)
        """
        quest_id = crud.get_current_question(self.db, tg_user_id)
        if quest_id is not None:
            quest = get_question(self.db, quest_id)
            return quest
        else:
            return None

    def edit_specialty(self, tg_user_id: int, new_specialty: Specialty) -> None:
        """
        Изменить в базе данных специальность пользователя
        """
        if is_tg_user_already_exist(self.db, tg_user_id):
            crud.edit_specialty(self.db, tg_user_id, new_specialty)
        else:
            raise UserNotExistsException("You try to add specialty for not exist user")

    def load_questions(self, specialty: Specialty, file: str) -> None:
        """
        Загрузить вопросы в базу данных из csv файла `file`
        """
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
        """
        Сбросить сессию (удалить все ответы пользователя, удалить сессию из базы данных)
        """
        # crud.remove_answers(self.db, user.tg_user_id)
        crud.remove_sessions(self.db, user.tg_user_id)
        # crud.remove_train_materials(self.db, user.tg_user_id)

    def add_bot_score(self, user: schemas.TelegramUser, bot_score: int) -> BotReview:
        """
        Добавить в базу данных оценку бота от пользователя
        """
        if bot_score not in range(1, 10):
            raise WrongBotScoreFormat("You can have only 1 to 10 score in field BotReview.bot_score")
        return crud.add_bot_score(self.db, user.tg_user_id, bot_score)

    def add_bot_review(self, user: schemas.TelegramUser, review: str, review_type: AnswerTypes) -> BotReview:
        """
        Добавить в базу данных ревью на бота от пользователя
        """
        return crud.add_bot_review(self.db, user.tg_user_id, review, review_type.name)

    def get_bot_review(self, user: schemas.TelegramUser) -> List[BotReview]:
        """
        Получить из базы данных список ревью на бота от пользователя
        """
        return crud.get_bot_review(self.db, user.tg_user_id)

    def add_problem_question_review(
        self, question_id: int, tg_user_id: int, review: str, review_type: AnswerTypes
    ) -> ProblemQuestionReview:
        """
        Добавить в базу данных ревью на вопрос question_id от пользователя с tg_user_id
        """
        return crud.add_problem_question_review(self.db, question_id, tg_user_id, review, review_type.name)

    def get_problem_question_review(self, tg_user_id: int) -> List[ProblemQuestionReview]:
        """
        Получить из базы данных список ревью на вопросы от пользователя с tg_user_id
        """
        return crud.get_problem_question_review(self.db, tg_user_id)

    def add_question_score(self, question_id: int, tg_user_id: int, score: int) -> QuestionScore:
        """
        Добавить в базу данных оценку вопроса question_id от пользователя с tg_user_id
        """
        return crud.add_question_score(self.db, question_id, tg_user_id, score)

    def get_question_score(self, question_id: int, tg_user_id: int) -> QuestionScore:
        """
        Получить из базы данных оценку вопроса question_id от пользователя с tg_user_id
        """
        return crud.get_question_score(self.db, question_id, tg_user_id)

    def get_all_questions_scores(self, tg_user_id: int) -> List[QuestionScore]:
        """
        Получить из базы данных оценки всех вопросов от пользователя с tg_user_id
        """
        return crud.get_questions_scores(self.db, tg_user_id)

    def remove_questions(self, specialty: str) -> None:
        """
        Удаляем из базы данных вопросы по заданной специальности [speciality]
        """
        crud.remove_questions(self.db, specialty)

    def remove_problem_question_review(self, tg_user_id: int, question_id: int) -> None:
        """
        Удаляем из базы данных ревью пользователя tg_user_id на вопрос question_id
        """
        crud.remove_problem_question_review(self.db, tg_user_id, question_id)

    def remove_question_score(self, question_id: int) -> None:
        """
        Удаляем из базы данных оценки вопроса с question_id
        """
        crud.remove_question_score(self.db, question_id)

    def remove_train_material(self, tg_user_id: int, question_id: int) -> None:
        """
        Удаляем из базы данных тренировочные материалы для пользователя tg_user_id по вопросу question_id
        """
        crud.remove_train_material(self.db, tg_user_id, question_id)
