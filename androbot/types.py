import aiogram.types as aiotypes
from pydantic.dataclasses import dataclass


class PydanticConfig:
    arbitrary_types_allowed = True


@dataclass(config=PydanticConfig)
class View:
    """
    Класс предназначен для подготовки ответа бота.
    Содержит текст ответа (в разметке Markdown), а также клавитуру,
    которую отправит бот в ответ в параметре reply_markup
    """

    text: str
    markup: aiotypes.ReplyKeyboardMarkup = None

    def __init__(self, text, markup=None):
        self.text = text
        self.markup = markup
