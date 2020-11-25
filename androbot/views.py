from dataclasses import dataclass

import aiogram.types as aiotypes

from .templates import render_message


@dataclass
class View:
    text: str
    markup: aiotypes.ReplyKeyboardMarkup = None


def get_main_menu(message: aiotypes.Message) -> View:
    template_file = r"templates/start.md"

    with open(template_file, "r", encoding="utf-8") as f:
        answer_text = f.read()

    btn_1 = aiotypes.KeyboardButton("Профиль")
    btn_2 = aiotypes.KeyboardButton("Android Developer")
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(
        btn_1, btn_2
    )

    return View(render_message(answer_text, message), reply_kb)


def get_hello_message(message: aiotypes.Message) -> View:
    template_file = r"templates/hello.md"

    with open(template_file, "r", encoding="utf-8") as f:
        answer_text = f.read()

    return View(render_message(answer_text, message))


def get_profile(message: aiotypes.Message) -> View:
    answer_text = "*{{username}}*\nВаш прогресс 5 из 10!\n"

    btn_1 = aiotypes.InlineKeyboardButton("Главное меню")
    btn_2 = aiotypes.InlineKeyboardButton("Метериалы для повторения")
    inline_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(
        btn_1, btn_2
    )

    return View(render_message(answer_text, message), inline_kb)
