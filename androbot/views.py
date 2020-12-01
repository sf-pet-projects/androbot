import aiogram.types as aiotypes

from .androbot_types import View
from .config import settings
from .templates import render_message


def get_main_menu(message: aiotypes.Message) -> View:
    """
    Возвращает View старатовой страницы бота
    """
    template_file = settings.static_folder / "start.md"

    with open(template_file, "r", encoding="utf-8") as f:
        answer_text = f.read()

    btn_1 = aiotypes.KeyboardButton("Android Developer")
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(btn_1)

    return View(render_message(answer_text, message), reply_kb)


def get_hello_message(message: aiotypes.Message) -> View:
    """
    Возвращает текст приветствия бота - новому пользователю
    """
    template_file = settings.static_folder / "hello.md"

    with open(template_file, "r", encoding="utf-8") as f:
        answer_text = f.read()

    return View(render_message(answer_text, message))
