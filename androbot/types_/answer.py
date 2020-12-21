from enum import Enum


class AnswerTypes(Enum):
    """
    Типы ответов
    """

    TEXT = "Текстом"
    VOICE = "Голосом"
    MENTAL = "Мысленно"
