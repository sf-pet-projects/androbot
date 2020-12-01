import aiogram.types as aiotypes

from .errors import UserExistsError


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
