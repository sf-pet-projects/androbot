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


def get_next_question(tg_user_id: int) -> View:
    """
    Возвращает View со следующим вопросом для пользователя
    """
    template_file = settings.static_folder / "question.md"

    with open(template_file, encoding="utf-8") as f:
        answer_text = f.read()

    try:
        question = actions.Actions().get_next_test(tg_user_id)
    except NoNewQuestionsException:
        reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        reply_kb.add(aiotypes.KeyboardButton("Главное меню"))

        return View("В базе не осталось новых вопросов", reply_kb)

    answer_text = render_message(answer_text, question=question.text_answer)

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(aiotypes.KeyboardButton("Далее"), aiotypes.KeyboardButton("Не понял вопрос"))

    return View(answer_text, reply_kb, question.quest_id)


def get_call_to_send_answer(answer_type: str) -> View:
    """
    Возвращает View с призывом написать ответ
    """
    template_file = settings.static_folder / "call_to_answer.md"

    with open(template_file, encoding="utf-8") as f:
        answer_text = f.read()

    answer_text = render_message(answer_text, answer_type=answer_type.lower())

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.add(aiotypes.KeyboardButton("Ответил мысленно"))

    return View(answer_text, reply_kb)


def get_do_not_understand_question() -> View:
    """
    Возвращает View с просбой написать что не понятного
    """
    template_file = settings.static_folder / "do_not_understand.md"

    with open(template_file, encoding="utf-8") as f:
        answer_text = f.read()

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.add(aiotypes.KeyboardButton("Отмена"))

    return View(answer_text, reply_kb)


def get_why_do_not_understand() -> View:
    """
    Возвращает View с просбой написать что не понятного
    """
    template_file = settings.static_folder / "why_do_not_understand.md"

    with open(template_file, encoding="utf-8") as f:
        answer_text = f.read()

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.add(aiotypes.KeyboardButton("Главное меню"))
    reply_kb.add(aiotypes.KeyboardButton("Решить другую задачу"))

    return View(answer_text, reply_kb)


def get_correct_answer(question_id: int) -> View:
    """
    Возвращает View с правильным ответом
    """
    template_file = settings.static_folder / "correct_answer.md"

    with open(template_file, encoding="utf-8") as f:
        answer_text = f.read()

    correct_answer = "42"
    answer_text = render_message(answer_text, correct_answer=correct_answer)

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.add(aiotypes.KeyboardButton("Главное меню"))
    reply_kb.add(aiotypes.KeyboardButton("Решить другую задачу"))

    return View(answer_text, reply_kb)
