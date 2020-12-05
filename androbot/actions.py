import aiogram.types as aiotypes

from .config import settings
from .errors import UserExistsError


def get_main_menu():
    return ["Android Developer"]


def start_new_test():
    return list(map(lambda x: x.strip(), settings.answers_types.split(",")))


def add_user(message: aiotypes.Message):
    """
    Добавляем нового пользователя в базу
    Если пользователь уже создан - вызываем исключение UserExistsError
    """
    import random

    if random.randint(0, 1) == 1:
        raise UserExistsError("User already exists", message)


def register_action(action: str, message: aiotypes.Message):
    """
    Регистрируем пользовательское событие в базе данных
    """
    pass
