import aiogram.types as aiotypes

from . import actions
from .errors import NoNewQuestionsException
from .templates import get_template, render_message
from .types_ import AnswerTypes, View


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


def get_android_developer_init_view(answer_type: str) -> View:
    """
    Возвращает View стартового экрана тестирования по специальности Андроид разработчик
    """
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(aiotypes.KeyboardButton("Отмена"), aiotypes.KeyboardButton("Готов!"))

    if answer_type == AnswerTypes.MENTAL.value:
        answer_way = "нажатием кнопки *Ответил мысленно*"
    elif answer_type == AnswerTypes.TEXT.value:
        answer_way = "отправкой текста"
    elif answer_type == AnswerTypes.VOICE.value:
        answer_way = "отправкой голосового сообщения"

    answer_text = render_message(get_template("android_developer"), answer_way=answer_way)

    return View(answer_text, reply_kb)


def get_select_answer_type_view() -> View:
    """
    Возвращает View в котором предлагает ответить, каким способом пользователь предпочитает отвечать
    """
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for answer_type in actions.start_new_test():
        btn = aiotypes.KeyboardButton(answer_type)
        reply_kb.add(btn)

    return View(get_template("select_answer_type"), reply_kb)


def get_next_question(tg_user_id: int, answer_type: str) -> View:
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

    if answer_type == AnswerTypes.MENTAL.value:
        call_to_action = "мысленно"
    elif answer_type == AnswerTypes.TEXT.value:
        call_to_action = "текстом"
    elif answer_type == AnswerTypes.VOICE.value:
        call_to_action = "голосом"

    answer_text = render_message(
        get_template("question"),
        question=question.text_question.strip(),
        question_category=question.question_category.strip(),
        call_to_action=call_to_action,
    )

    row_buttons = [aiotypes.KeyboardButton("Не понял вопрос")]
    if answer_type == AnswerTypes.MENTAL.value:
        row_buttons.append(aiotypes.KeyboardButton("Ответил мысленно."))

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(*row_buttons)

    return View(answer_text, reply_kb, question.id)


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
        correct_answer = act.get_test_result(tg_user_id).text_answer.strip()

    if not correct_answer:
        correct_answer = "К сожалению мы не подготовили правильный ответ на данный вопрос"

    answer_text = render_message(get_template("correct_answer"), correct_answer=correct_answer)

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.add(aiotypes.KeyboardButton("Главное меню"))
    reply_kb.add(aiotypes.KeyboardButton("Решить другую задачу"))

    return View(answer_text, reply_kb)
