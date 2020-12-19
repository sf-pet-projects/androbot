import aiogram.types as aiotypes

from . import actions
from .errors import NoNewQuestionsException
from .templates import get_template, render_message
from .types_ import View


def get_main_menu() -> View:
    """
    Возвращает View старатовой страницы бота
    """
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for speciality in actions.get_main_menu():
        btn_1 = aiotypes.KeyboardButton(speciality)
        reply_kb.add(btn_1)

    return View(get_template("start"), reply_kb)


def get_hello_message(username: str) -> View:
    """
    Возвращает текст приветствия бота - новому пользователю
    """
    return View(render_message(get_template("hello"), username=username))


def get_android_developer_init_view() -> View:
    """
    Возвращает View стартового экрана тестирования по специальности Андроид разработчик
    """
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(aiotypes.KeyboardButton("Готов!"), aiotypes.KeyboardButton("Отмена"))

    return View(get_template("android_developer"), reply_kb)


def get_select_answer_type_view() -> View:
    """
    Возвращает View в котором предлагает ответить, каким способом пользователь предпочитает отвечать
    """
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for answer_type in actions.start_new_test():
        btn = aiotypes.KeyboardButton(answer_type)
        reply_kb.add(btn)

    return View(get_template("select_answer_type"), reply_kb)


def get_next_question(tg_user_id: int) -> View:
    """
    Возвращает View со следующим вопросом для пользователя
    """
    try:
        with actions.Actions() as act:
            question = act.get_next_test(tg_user_id)

    except NoNewQuestionsException:
        reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        reply_kb.add(aiotypes.KeyboardButton("Главное меню"))

        return View("В базе не осталось новых вопросов", reply_kb)

    answer_text = render_message(
        get_template("question"),
        question=question.text_question,
        question_category=question.question_category,
    )

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(aiotypes.KeyboardButton("Далее"), aiotypes.KeyboardButton("Не понял вопрос"))

    return View(answer_text, reply_kb, question.id)


def get_call_to_send_answer(answer_type: str) -> View:
    """
    Возвращает View с призывом написать ответ
    """
    answer_text = render_message(get_template("call_to_answer"), answer_type=answer_type.lower())

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.add(aiotypes.KeyboardButton("Ответил мысленно"))

    return View(answer_text, reply_kb)


def get_do_not_understand_question() -> View:
    """
    Возвращает View с просбой написать что не понятного
    """
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.add(aiotypes.KeyboardButton("Отмена"))

    return View(get_template("do_not_understand"), reply_kb)


def get_why_do_not_understand() -> View:
    """
    Возвращает View с просбой написать что не понятного
    """
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.add(aiotypes.KeyboardButton("Главное меню"))
    reply_kb.add(aiotypes.KeyboardButton("Решить другую задачу"))

    return View(get_template("why_do_not_understand"), reply_kb)


def get_correct_answer(tg_user_id: int) -> View:
    """
    Возвращает View с правильным ответом
    """
    with actions.Actions() as act:
        correct_answer = act.get_test_result(tg_user_id)

    answer_text = render_message(get_template("correct_answer"), correct_answer=correct_answer)

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.add(aiotypes.KeyboardButton("Главное меню"))
    reply_kb.add(aiotypes.KeyboardButton("Решить другую задачу"))

    return View(answer_text, reply_kb)
