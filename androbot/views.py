import aiogram.types as aiotypes

from .actions import Actions, get_main_menu, start_new_test
from .errors import NoNewQuestionsException
from .templates import get_template, render_message
from .types_ import AnswerTypes, DialogueStates, View


def get_hello_message(username: str) -> View:
    """
    Возвращает текст приветствия бота - новому пользователю
    """
    return View(render_message(get_template("01_hello"), username=username))


def get_main_menu_view() -> View:
    """
    Возвращает View старатовой страницы бота
    """
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for speciality in get_main_menu():
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
    for answer_type in reversed(start_new_test()):
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
        with Actions() as act:
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
        aiotypes.KeyboardButton("🤷‍♂️ Не понял вопрос"),
        aiotypes.KeyboardButton("🙅🏻‍♀️ Не знаю ответ"),
    ]

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(*row_buttons)

    return View(answer_text, reply_kb, question.id)


def get_why_do_not_understand() -> View:
    """
    Возвращает View с просбой написать что не понятного
    """
    return View(get_template("31_why_do_not_understand"))


def get_correct_answer(tg_user_id: int) -> View:
    """
    Возвращает View с правильным ответом
    """
    with Actions() as act:
        correct_answer = act.get_current_question(tg_user_id).text_answer.strip().replace("_", "\\_")

    if not correct_answer:
        answer_text = render_message(get_template("40_no_correct_answer"))
        row_buttons = [
            aiotypes.KeyboardButton("📚 Отправь материалы"),
            aiotypes.KeyboardButton("➡️ Следующий вопрос"),
        ]
        state = DialogueStates.NO_ANSWER
    else:
        answer_text = render_message(get_template("41_correct_answer"), correct_answer=correct_answer)
        row_buttons = [
            aiotypes.KeyboardButton("❌ Неверный"),
            aiotypes.KeyboardButton("⚖️ Частично верный"),
            aiotypes.KeyboardButton("✅ Верный"),
        ]
        state = DialogueStates.GOT_ANSWER

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(*row_buttons)

    return View(answer_text, reply_kb, state=state)


def get_do_you_want_additional_materials_view() -> View:
    """
    Возвращает View с предолжением дополнительных материалов
    """

    answer_text = render_message(get_template("42_do_you_want_additional_materials"))

    row_buttons = [
        aiotypes.KeyboardButton("📚 Отправь материалы"),
        aiotypes.KeyboardButton("➡️ Следующий вопрос"),
    ]

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(*row_buttons)

    return View(answer_text, reply_kb)


def get_additional_materials_view(tg_user_id: int) -> View:
    """
    Возвращает View с дополнительными материалами
    """
    with Actions() as act:
        additional_info = act.get_current_question(tg_user_id).additional_info.strip().replace("_", "\\_")

    if not additional_info:
        additional_info = "К сожалению мы не подготовили материалы к этому вопросу"
    else:
        additional_info = "Материалы для повторения...\n{}\n".format(additional_info)

    answer_text = render_message(get_template("46_additional_materials"), additional_info=additional_info)

    row_buttons = [
        aiotypes.KeyboardButton("➡️ Следующий вопрос"),
    ]

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(*row_buttons)

    return View(answer_text, reply_kb)


def get_do_you_want_to_get_correct_answer() -> View:
    """
    Возвращает View с предолжением узнать эталонный ответ, или идти дальше
    """

    answer_text = render_message(get_template("45_do_you_want_to_get_correct_answer"))

    row_buttons = [
        aiotypes.KeyboardButton("💡 Эталонный ответ"),
        aiotypes.KeyboardButton("➡️ Следующий вопрос"),
    ]

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(*row_buttons)

    return View(answer_text, reply_kb)


def get_user_score_view(user_id: int):
    """
    Возвращает view оценки пользователя
    """

    with Actions() as act:
        user_scores = act.get_questions_scores(user_id)

    # score 0 - неверно, 1 - частично верно, 2 - верно
    user_score = int(sum(x.score for x in user_scores) / len(user_scores) / 2 * 100)

    if user_score > 84:
        user_score_description = (
            "Поздравляем! Вы готовы к прохождению технического собеседования! Самое время "
            "опубликовать резюме, откликнуться на пару вакансий и двигаться вперед к своим целям."
        )
    elif user_score > 69:
        user_score_description = (
            "Отличный результат. Мы рекомендуем вам пройтись еще раз по верхам, решить пару "
            "общих практических задач и смело публиковать резюме для прохождения технических"
            " собеседований. Вперед к мечте!"
        )
    else:
        user_score_description = (
            "Хороший результат. Мы рекомендуем повторить все основные темы, отдельно по "
            "каждой решить пару практических задач и освежить основные знания теории. А "
            "потом вернуться к нашему боту еще раз. Будем вас ждать :)"
        )

    answer_text = render_message(
        get_template("51_user_score"), user_score=user_score, user_score_description=user_score_description
    )

    row_buttons = [
        aiotypes.KeyboardButton("👍 Оценить бота"),
        aiotypes.KeyboardButton("🏠 Главное меню"),
    ]

    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reply_kb.row(*row_buttons)

    return View(answer_text, reply_kb)
