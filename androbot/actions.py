import codecs

from loguru import logger

from . import SessionLocal, crud, schemas
from .config import settings
from .crud import is_tg_user_already_exist
from .errors import UserExistsException, UserNotExistsException
from .specialty import Specialty


def get_main_menu():
    with codecs.open("welcome.message", "r", encoding="utf-8") as file:
        welcome_message = file.read()
        return [welcome_message, [e.value for e in Specialty]]


def start_new_test():
    return list(map(lambda x: x.strip(), settings.answers_types.split(",")))


def add_user(tg_user: schemas.TelegramUser):
    db = SessionLocal()
    if is_tg_user_already_exist(db, tg_user.tg_user_id):
        return UserExistsException
    else:
        db_user = crud.create_tg_user(db, tg_user)
        logger.info("Add new telegram user {}", tg_user)
    db.close()
    return db_user


def remove_user(tg_user: schemas.TelegramUser):
    db = SessionLocal()
    if is_tg_user_already_exist(db, tg_user.tg_user_id):
        crud.remove_tg_user(db, tg_user)
        logger.info(
            "Remove telegram user tg_user_id={}, name={}, username={}",
            tg_user.tg_user_id,
            tg_user.name,
            tg_user.username,
        )
    else:
        return UserNotExistsException
    db.close()
