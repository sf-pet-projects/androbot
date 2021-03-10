import aiogram.types as aiotypes

from . import actions
from .errors import NoNewQuestionsException
from .templates import get_template, render_message
from .types_ import AnswerTypes, View


def get_hello_message(username: str) -> View:
    """
    Возвращает текст приветствия бота - новому пользователю
    """
    return View(render_message(get_template("01_hello"), username=username))


def get_main_menu() -> View:
    """
    Возвращает View старатовой страницы бота
    """
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for speciality in actions.get_main_menu():
        btn_1 = aiotypes.KeyboardButton(f"✅ {speciality}")
        reply_kb.add(btn_1)

    return View(get_template("02_start"), reply_kb)


def get_do_you_want_to_reset_test_view() -> View:
    """
    Возвращает View в котором спрашивает, нужно ли продолжить начатный тест, или начать сначала
    """
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    row_buttons = [
        aiotypes.KeyboardButton("🏠 Главное меню"),
        aiotypes.KeyboardButton("🔄 Начать с начала"),
        aiotypes.KeyboardButton("✅ Продолжить"),
    ]
    reply_kb.row(*row_buttons)

    return View(get_template("03_do_you_want_to_reset_test"), reply_kb)


def get_resetting_test_view() -> View:
    """
    Возвращает View в котором уведомляет о сбросе тестирования
    """
    return View(get_template("04_resetting_test"))


def get_select_answer_type_view() -> View:
    """
    Возвращает View в котором предлагает ответить, каким способом пользователь предпочитает отвечать
    """
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    row_buttons = []
    for answer_type in reversed(actions.start_new_test()):
        btn = aiotypes.KeyboardButton(answer_type)
        row_buttons.append(btn)
    reply_kb.row(*row_buttons)

    return View(get_template("05_select_answer_type"), reply_kb)


def get_are_you_ready_for_test_view(answer_type: str) -> View:
    """
    Возвращает View стартового экрана тестирования по специальности Андроид разработчик
    """
    if answer_type == AnswerTypes.TEXT.value:
        answer_way = "отправкой текста"
    elif answer_type == AnswerTypes.VOICE.value:
        answer_way = "отправкой голосового сообщения"
    answer_text = render_message(get_template("09_are_you_ready_for_test"), answer_way=answer_way)

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(aiotypes.KeyboardButton("🚫 Отмена"), aiotypes.KeyboardButton("✅ Готов!"))

    return View(answer_text, reply_kb)


def get_next_question(tg_user_id: int, answer_type: str) -> View:
    """
    Возвращает View со следующим вопросом для пользователя
    """
    try:
        with actions.Actions() as act:
            question = act.get_next_test(tg_user_id)

    except NoNewQuestionsException:
        reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        reply_kb.add(aiotypes.KeyboardButton("🏠 Главное меню"))

        return View("В базе не осталось новых вопросов", reply_kb)

    if answer_type == AnswerTypes.TEXT.value:
        call_to_action = "текстом"
    elif answer_type == AnswerTypes.VOICE.value:
        call_to_action = "голосом"

    answer_text = render_message(
        get_template("20_question"),
        question=question.text_question.strip(),
        question_category=question.question_category.strip(),
        call_to_action=call_to_action,
    )

    row_buttons = [
        aiotypes.KeyboardButton("🤷‍♂️Не понял вопрос"),
        aiotypes.KeyboardButton("🙅🏻‍♀️ Не знаю ответ"),
    ]

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(*row_buttons)

    return View(answer_text, reply_kb, question.id)


def get_do_not_understand_question(answer_type) -> View:
    """
    Возвращает View с просбой написать что не понятного
    """
    if answer_type == AnswerTypes.TEXT.value:
        call_to_action = "текстом"
    elif answer_type == AnswerTypes.VOICE.value:
        call_to_action = "голосом"

    additional_info = "Тут будет доп.информация"

    answer_text = render_message(
        get_template("30_do_not_understand"),
        additional_info=additional_info,
        call_to_action=call_to_action,
    )
    row_buttons = [
        aiotypes.KeyboardButton("🤷‍♂️Все равно не понятно"),
        aiotypes.KeyboardButton("🙅🏻‍♀️ Не знаю ответ"),
    ]

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(*row_buttons)

    return View(answer_text, reply_kb)


def get_still_not_understand() -> View:
    """
    Возвращает View с просбой написать что не понятного
    """
    return View(get_template("31_still_not_understand"))


def get_why_do_not_understand() -> View:
    """
    Возвращает View после отправки сообщения что не понятно
    """
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.add(aiotypes.KeyboardButton("🏠 Главное меню"))
    reply_kb.add(aiotypes.KeyboardButton("Решить другую задачу"))

    return View(get_template("32_why_do_not_understand"), reply_kb)


def get_correct_answer(tg_user_id: int) -> View:
    """
    Возвращает View с правильным ответом
    """
    with actions.Actions() as act:
        correct_answer = act.get_current_question(tg_user_id).text_answer.strip()

    if not correct_answer:
        correct_answer = "К сожалению мы не подготовили правильный ответ на данный вопрос"

    answer_text = render_message(get_template("40_correct_answer"), correct_answer=correct_answer)

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.add(aiotypes.KeyboardButton("🏠 Главное меню"))
    reply_kb.add(aiotypes.KeyboardButton("Решить другую задачу"))

    return View(answer_text, reply_kb)
