import aiogram.types as aiotypes

from .templates import render_message
from .types import View


def get_main_menu(message: aiotypes.Message) -> View:
    template_file = r"templates/start.md"

    with open(template_file, "r", encoding="utf-8") as f:
        answer_text = f.read()

    btn_1 = aiotypes.KeyboardButton("Android Developer")
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(btn_1)

    return View(render_message(answer_text, message), reply_kb)


def get_hello_message(message: aiotypes.Message) -> View:
    template_file = r"templates/hello.md"

    with open(template_file, "r", encoding="utf-8") as f:
        answer_text = f.read()

    return View(render_message(answer_text, message))
