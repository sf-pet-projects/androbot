from aiogram import types as aiotypes
from loguru import logger


class BaseAppError(Exception):
    def __init__(self, message_text: str, message: aiotypes.Message) -> None:
        super().__init__(message_text)
        self.message = message
        self.message_text = message_text

    def __str__(self) -> str:
        return self.message_text

    @property
    def response(self) -> str:
        return "Нам жаль, но произошла непредвиденная ошибка. Пожалуйста, напишите @Ruppe об этом."


class ErrorExample(BaseAppError):
    @property
    def response(self) -> str:
        return "Error error"


class UserExistsException(BaseAppError):
    @property
    def response(self) -> str:
        logger.warning("You try to add already exists user")
        return "You try to add already exists user"


class UserNotExistsException(BaseAppError):
    @property
    def response(self) -> str:
        logger.warning("You try to remove doesn't exist user")
        return "You try to remove doesn't exist user"
