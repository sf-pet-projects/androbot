class BaseAppError(Exception):
    def __init__(self, message_text: str) -> None:
        super().__init__(message_text)
        self.message_text = message_text

    def __str__(self) -> str:
        return self.message_text


class UserExistsException(BaseAppError):
    pass


class UserNotExistsException(BaseAppError):
    pass


class NoNewQuestionsException(BaseAppError):
    pass


class TemplateNotFound(BaseAppError):
    pass


class TooManyParamsForLoggingActions(BaseAppError):
    pass


class WrongBotScoreFormat(BaseAppError):
    pass


class NoCurrentSessionException(BaseAppError):
    pass
