from dataclasses import dataclass
from typing import Union

import aiogram.types as aiotypes

from .templates import render_message


@dataclass
class View:
    text: str
    markup: aiotypes.InlineKeyboardMarkup


def get_main_menu(message: Union[aiotypes.Message, aiotypes.CallbackQuery]) -> View:
    template_file = r"templates/start.md"

    with open(template_file, "r", encoding="utf-8") as f:
        answer_text = f.read()

    btn_1 = aiotypes.InlineKeyboardButton("Профиль", callback_data="open_profile")
    btn_2 = aiotypes.InlineKeyboardButton("Android Developer", callback_data="android_developer")
    inline_kb = aiotypes.InlineKeyboardMarkup().add(btn_1, btn_2)

    return View(render_message(answer_text, message), inline_kb)


def get_profile(message: aiotypes.Message) -> View:
    answer_text = "*{{username}}*\nВаш прогресс 5 из 10!\n"

    btn_1 = aiotypes.InlineKeyboardButton("Главное меню", callback_data="main_menu")
    btn_2 = aiotypes.InlineKeyboardButton(
        "Метериалы для повторения", callback_data="povtor_materials"
    )
    inline_kb = aiotypes.InlineKeyboardMarkup().add(btn_1, btn_2)

    return View(render_message(answer_text, message), inline_kb)
