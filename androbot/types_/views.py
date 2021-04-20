from typing import Optional

import aiogram.types as aiotypes
from pydantic.dataclasses import dataclass

from . import DialogueStates


class PydanticConfig:
    arbitrary_types_allowed = True


@dataclass(config=PydanticConfig)
class View:
    """
    Класс предназначен для подготовки ответа бота.
    Содержит текст ответа (в разметке Markdown), а также клавитуру,
    которую отправит бот в ответ в параметре reply_markup
    и состояние бота, которое нужно установить в результате
    """

    text: str
    markup: Optional[aiotypes.ReplyKeyboardMarkup] = None
    question_id: Optional[int] = None
    state: Optional[DialogueStates] = None

    def __init__(
        self,
        text: str,
        markup: Optional[aiotypes.ReplyKeyboardMarkup] = None,
        question_id: Optional[int] = None,
        state: Optional[DialogueStates] = None,
    ):
        self.text = text
        self.markup = markup
        self.question_id = question_id
        self.state = state
