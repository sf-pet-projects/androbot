from aiogram import types as aiotypes
from aiogram.dispatcher import FSMContext

from . import schemas, views
from .actions import Actions, start_new_test
from .errors import UserExistsException
from .main import bot, dp
from .types_ import AnswerTypes, DialogueStates, Events, Specialty, UserScore
from .utils import log_event


@dp.message_handler(commands=["start"], state="*")
async def send_start_screen(message: aiotypes.Message):
    """
    Обработчик для команды start.
    """
    full_user_name = " ".join((name for name in [message.from_user.first_name, message.from_user.last_name] if name))
    tg_user = schemas.TelegramUser(
        tg_user_id=message.from_user.id, name=full_user_name, username=message.from_user.username
    )

    try:
        with Actions() as act:
            act.add_user(tg_user)
        view = views.get_hello_message(full_user_name)
        await bot.send_message(
            text=view.text,
            chat_id=message.chat.id,
            parse_mode=aiotypes.ParseMode.MARKDOWN,
            reply_markup=view.markup,
        )

        log_event(message.from_user.id, Events.Registration, message.text.replace("/start ", ""))

    except UserExistsException:
        pass

    view = views.get_main_menu_view()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    log_event(message.from_user.id, Events.Start)

    await DialogueStates.MAIN_MENU.set()


@dp.message_handler(regexp="Android Developer", state=DialogueStates.MAIN_MENU)
async def after_select_speciality(message: aiotypes.Message, state: FSMContext):
    """
    Проверяем что тест еще не начат.
    Предагаем выбрать cпособ ответа
    """

    new_speciality = Specialty.ANDROID

    await state.update_data(speciality=new_speciality.value)

    log_event(message.from_user.id, Events.Speciality, new_speciality.value)

    with Actions() as act:
        act.edit_specialty(message.from_user.id, new_speciality)

        if act.has_started_test(message.from_user.id):
            view = views.get_do_you_want_to_reset_test_view()

            await bot.send_message(
                text=view.text,
                chat_id=message.chat.id,
                parse_mode=aiotypes.ParseMode.MARKDOWN,
                reply_markup=view.markup,
            )

            log_event(message.from_user.id, Events.AlreadyTried, new_speciality.value)

            await DialogueStates.next()
        else:
            await select_answer_type(message)


@dp.message_handler(regexp="Начать с начала", state=DialogueStates.HAS_STARTED_TEST)
async def reset_test_progress(message: aiotypes.Message, state: FSMContext):
    """
    Сбрасываем отвеченные вопросы, и начинаем отвечать заново
    """
    state_data = await state.get_data()
    log_event(message.from_user.id, Events.ResetProgress, state_data["speciality"])

    with Actions() as act:
        tg_user = schemas.TelegramUser(
            tg_user_id=message.from_user.id,
            name=message.from_user.username,
            username=message.from_user.username,
        )
        act.reset_session(tg_user)

    view = views.get_resetting_test_view()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await select_answer_type(message)


@dp.message_handler(regexp="Продолжить", state=DialogueStates.HAS_STARTED_TEST)
async def continue_test(message: aiotypes.Message, state: FSMContext):
    """
    Продолжаем отвечать на вопросы теста
    """
    state_data = await state.get_data()
    log_event(message.from_user.id, Events.ContinueTask, state_data["speciality"])

    await select_answer_type(message)


async def select_answer_type(message: aiotypes.Message):
    """
    Предлагает выбрать способ ответа на вопросы
    """

    view = views.get_select_answer_type_view()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await DialogueStates.SELECT_ANSWER_TYPE.set()


@dp.message_handler(state=DialogueStates.SELECT_ANSWER_TYPE)
async def after_select_answer_type(message: aiotypes.Message, state: FSMContext):
    """
    Проверяем что-за вариант ответа он выбрал.
    Если ОК, задаем первый вопрос.
    """

    answer_type = message.text.title()
    if answer_type not in start_new_test():
        await message.reply("Ты выбрал некорректный вариант. Попробуй еще раз.", reply=False)
        return

    view = views.get_are_you_ready_for_test_view(answer_type)

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    state_data = await state.get_data()
    log_event(message.from_user.id, Events.AnswerType, state_data["speciality"], answer_type)

    await state.update_data(answer_type=answer_type)

    await DialogueStates.next()


@dp.message_handler(
    regexp="Отмена|Главное меню",
    state=[
        DialogueStates.ARE_YOU_READY_FOR_TEST,
        DialogueStates.NO_ANSWER,
        DialogueStates.ANSWER_SCORED_BY_USER,
        DialogueStates.HAS_STARTED_TEST,
        DialogueStates.USER_SCORE,
    ],
)
async def back_to_main_menu(message: aiotypes.Message):
    """
    Возвращаемся в главное меню
    """
    view = views.get_main_menu_view()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    log_event(message.from_user.id, Events.Start)

    await DialogueStates.MAIN_MENU.set()


@dp.message_handler(
    regexp="Готов!|Следующий вопрос",
    state=[
        DialogueStates.ARE_YOU_READY_FOR_TEST,
        DialogueStates.NO_ANSWER,
        DialogueStates.ANSWER_SCORED_BY_USER,
        DialogueStates.DO_YOU_WANT_GET_ANSWER,
    ],
)
async def get_another_question(message: aiotypes.Message, state: FSMContext):
    """
    Выдать пользователю задачу
    """
    state_data = await state.get_data()

    view = views.get_next_question(message.from_user.id, state_data["answer_type"])

    if not view.question_id:
        await show_user_score(message, state)
        return

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    log_event(message.from_user.id, Events.TaskStart, state_data["speciality"], view.question_id)

    await state.update_data(question_id=view.question_id)

    await DialogueStates.ASK_QUESTION.set()


@dp.message_handler(regexp="Не понял вопрос", state=DialogueStates.ASK_QUESTION)
async def not_understand_question(message: aiotypes.Message, state: FSMContext):
    """
    Пользователю не понятен вопрос, спросим почему не понятен
    """
    state_data = await state.get_data()

    answer = schemas.Answer(
        quest_id=state_data["question_id"],
        tg_user_id=message.from_user.id,
        answer_type=state_data["answer_type"],
        text_answer=message.text,
    )

    with Actions() as act:
        act.add_answer(answer)

    view = views.get_why_do_not_understand()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await DialogueStates.DO_NOT_UNDERSTAND.set()


@dp.message_handler(state=DialogueStates.DO_NOT_UNDERSTAND)
async def get_why_not_understand_question(message: aiotypes.Message, state: FSMContext):
    """
    Получили описание, почему вопрос не понятен
    """
    state_data = await state.get_data()

    log_event(
        message.from_user.id,
        Events.Unclear,
        state_data["speciality"],
        state_data["question_id"],
        message.text,
    )

    with Actions() as act:
        act.add_problem_question_review(
            state_data["question_id"], message.from_user.id, message.text, AnswerTypes(state_data["answer_type"])
        )

    view = views.get_do_you_want_to_get_correct_answer()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await DialogueStates.DO_YOU_WANT_GET_ANSWER.set()


@dp.message_handler(regexp="Не знаю ответ", state=DialogueStates.ASK_QUESTION)
async def do_not_know_question(message: aiotypes.Message, state: FSMContext):
    """
    Не знает ответ на вопрос.
    Хочет ли посмотреть эталонный ответ, или следующий вопрос зададим
    """

    state_data = await state.get_data()

    answer = schemas.Answer(
        quest_id=state_data["question_id"],
        tg_user_id=message.from_user.id,
        answer_type=state_data["answer_type"],
        text_answer=message.text,
    )

    with Actions() as act:
        act.add_question_score(state_data["question_id"], message.from_user.id, score=0)
        act.add_answer(answer)

    log_event(
        message.from_user.id,
        Events.DontKnow,
        state_data["speciality"],
        state_data["question_id"],
    )

    view = views.get_do_you_want_to_get_correct_answer()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await DialogueStates.DO_YOU_WANT_GET_ANSWER.set()


@dp.message_handler(
    content_types=[aiotypes.ContentType.TEXT, aiotypes.ContentType.VOICE],
    state=DialogueStates.ASK_QUESTION,
)
async def get_answer_from_user(message: aiotypes.Message, state: FSMContext):
    """
    Читает ответ пользователя
    """
    state_data = await state.get_data()

    answer_type = state_data["answer_type"]
    is_voice_answer = answer_type == AnswerTypes.VOICE.value
    is_text_answer = answer_type == AnswerTypes.TEXT.value

    if is_voice_answer and message.content_type != aiotypes.ContentType.VOICE:
        await message.reply("Ты выбрал вариант - отвечать голосом. Продиктуй ответ.")
        return
    elif is_text_answer and message.content_type != aiotypes.ContentType.TEXT:
        await message.reply("Ты выбрал вариант - отвечать текстом. Напиши ответ.")
        return

    voice_id = None
    if is_voice_answer:
        voice_id = message.voice.file_id

    answer = schemas.Answer(
        quest_id=state_data["question_id"],
        tg_user_id=message.from_user.id,
        answer_type=answer_type,
        text_answer=message.text,
        link_to_audio_answer=voice_id,
    )

    with Actions() as act:
        act.add_answer(answer)

    log_event(
        message.from_user.id,
        Events.SendSolution,
        state_data["speciality"],
        state_data["question_id"],
        voice_id or message.text,
        state_data["answer_type"],
    )

    view = views.get_correct_answer(message.from_user.id)

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    if view.state:
        await view.state.set()


@dp.message_handler(regexp="Эталонный ответ", state=DialogueStates.DO_YOU_WANT_GET_ANSWER)
async def send_correct_answer_to_user(message: aiotypes.Message):
    """
    Отправляет эталонный ответ пользователю
    """

    view = views.get_correct_answer(message.from_user.id)

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    if view.state:
        await view.state.set()


@dp.message_handler(regexp="|".join(score.description for score in UserScore), state=DialogueStates.GOT_ANSWER)
async def get_self_score_by_user(message: aiotypes.Message, state: FSMContext):
    """
    Получаем и записываем оценку от пользователя, предлагаем материалы для повторения
    """
    state_data = await state.get_data()

    answer_score = UserScore.by_description(message.text)

    with Actions() as act:
        act.add_question_score(state_data["question_id"], message.from_user.id, answer_score.value)

    view = views.get_do_you_want_additional_materials_view()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await DialogueStates.ANSWER_SCORED_BY_USER.set()


@dp.message_handler(regexp="Отправь материалы", state=[DialogueStates.NO_ANSWER, DialogueStates.ANSWER_SCORED_BY_USER])
async def send_additional_materials_to_user(message: aiotypes.Message, state: FSMContext):
    """
    Отправляет дополнительные материалы по вопросу
    """

    view = views.get_additional_materials_view(message.from_user.id)

    state_data = await state.get_data()

    with Actions() as act:
        act.add_train_material(state_data["question_id"], message.from_user.id)

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )


async def show_user_score(message: aiotypes.Message, state: FSMContext):
    """
    Вопросы кончились, покажем пользователю его оценку. Больше вопрос нет
    """

    state_data = await state.get_data()

    with Actions() as act:
        count_got_additional_materials = len(act.get_train_material(message.from_user.id))

    log_event(message.from_user.id, Events.FinishSpeciality, state_data["speciality"], count_got_additional_materials)

    view = views.get_user_score_view(message.from_user.id)

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await DialogueStates.USER_SCORE.set()
