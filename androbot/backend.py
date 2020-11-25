import aiogram.types as aiotypes

from .errors import UserExistsError


def add_user(message: aiotypes.Message):
    import random

    if random.randint(0, 1) == 1:
        raise UserExistsError("User already exists", message)


def register_action(action: str, message: aiotypes.Message):
    pass
