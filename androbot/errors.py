from aiogram import types as aiotypes


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


class UserExistsError(BaseAppError):
    """
    Возникает когда пытаемся добавить пользователя, который уже существует в базе
    """

    pass
