import aiogram.types as aiotypes

from . import actions
from .config import settings
from .templates import render_message
from .types_ import View


def get_main_menu(message: aiotypes.Message) -> View:
    """
    Возвращает View старатовой страницы бота
    """
    template_file = settings.static_folder / "start.md"

    with open(template_file, encoding="utf-8") as f:
        answer_text = f.read()

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for speciality in actions.get_main_menu():
        btn_1 = aiotypes.KeyboardButton(speciality)
        reply_kb.add(btn_1)

    return View(render_message(answer_text, message), reply_kb)


def get_hello_message(message: aiotypes.Message) -> View:
    """
    Возвращает текст приветствия бота - новому пользователю
    """
    template_file = settings.static_folder / "hello.md"

    with open(template_file, encoding="utf-8") as f:
        answer_text = f.read()

    return View(render_message(answer_text, message))


def get_android_developer_init_view(message: aiotypes.Message) -> View:
    """
    Возвращает View стартового экрана тестирования по специальности Андроид разработчик
    """
    template_file = settings.static_folder / "android_developer.md"

    with open(template_file, encoding="utf-8") as f:
        answer_text = f.read()

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(aiotypes.KeyboardButton("Готов!"), aiotypes.KeyboardButton("Отмена"))

    return View(render_message(answer_text, message), reply_kb)


def get_select_answer_type_view(message: aiotypes.Message) -> View:
    """
    Возвращает View в котором предлагает ответить, каким способом пользователь предпочитает отвечать
    """
    template_file = settings.static_folder / "select_answer_type.md"

    with open(template_file, encoding="utf-8") as f:
        answer_text = f.read()

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for answer_type in actions.start_new_test():
        btn = aiotypes.KeyboardButton(answer_type)
        reply_kb.add(btn)

    return View(render_message(answer_text, message), reply_kb)
