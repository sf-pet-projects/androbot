import aiogram.types as aiotypes

from . import actions
from .config import settings
from .errors import NoNewQuestionsException
from .templates import render_message
from .types_ import View


def get_main_menu() -> View:
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

    return View(answer_text, reply_kb)


def get_hello_message(username: str) -> View:
    """
    Возвращает текст приветствия бота - новому пользователю
    """
    template_file = settings.static_folder / "hello.md"

    with open(template_file, encoding="utf-8") as f:
        answer_text = f.read()

    return View(render_message(answer_text, username=username))


def get_android_developer_init_view() -> View:
    """
    Возвращает View стартового экрана тестирования по специальности Андроид разработчик
    """
    template_file = settings.static_folder / "android_developer.md"

    with open(template_file, encoding="utf-8") as f:
        answer_text = f.read()

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(aiotypes.KeyboardButton("Готов!"), aiotypes.KeyboardButton("Отмена"))

    return View(answer_text, reply_kb)


def get_select_answer_type_view() -> View:
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

    return View(answer_text, reply_kb)


def get_next_question(tg_user_id) -> View:
    """
    Возвращает View со следующим вопросом для пользователя
    """
    template_file = settings.static_folder / "question.md"

    with open(template_file, encoding="utf-8") as f:
        answer_text = f.read()

    try:
        question = actions.Actions().get_next_test(tg_user_id)
        answer_text = render_message(answer_text, question=question.text_answer)
    except NoNewQuestionsException:
        return View("В базе не осталось новых вопросов")

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(aiotypes.KeyboardButton("Далее"), aiotypes.KeyboardButton("Не понял вопрос"))

    return View(answer_text, reply_kb, question.quest_id)
