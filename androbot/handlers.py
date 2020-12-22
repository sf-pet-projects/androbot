from aiogram import types as aiotypes
from aiogram.dispatcher import FSMContext

from . import schemas, views
from .actions import Actions, start_new_test
from .errors import UserExistsException
from .main import bot, dp
from .types_ import AnswerTypes, DialogueStates


@dp.message_handler(commands=["start"], state="*")
async def send_start_screen(message: aiotypes.Message):
    """
    Обработчик для команды start.
    """
    full_user_name = " ".join(
        (name for name in [message.from_user.first_name, message.from_user.last_name] if name)
    )
    tg_user = schemas.TelegramUser(
        tg_user_id=message.from_user.id,
        name=full_user_name,
        username=message.from_user.username,
        specialty="Android Developer",  # TODO это не должно быть обязательным полем
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

    except UserExistsException:
        pass

    view = views.get_main_menu()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await DialogueStates.MAIN_MENU.set()


@dp.message_handler(text="Android Developer", state=DialogueStates.MAIN_MENU)
async def show_select_answer_type(message: aiotypes.Message):
    """
    Предагаем выбрать вариант ответа
    """

    view = views.get_select_answer_type_view()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await DialogueStates.next()


@dp.message_handler(state=DialogueStates.SELECT_ANSWER_TYPE)
async def show_call_to_start_test(message: aiotypes.Message, state: FSMContext):
    """
    Проверяем что-за вариант ответа он выбрал.
    Если ОК, задаем первый вопрос.
    """

    if message.text.title() not in start_new_test():
        await message.reply("Ты выбрал некорректный вариант. Попробуй еще раз.", reply=False)
        return

    await state.update_data(answer_type=message.text.title())

    view = views.get_android_developer_init_view()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await DialogueStates.next()


@dp.message_handler(text="Отмена", state=DialogueStates.ANDROID_DEVELOPER_INIT_VIEW)
@dp.message_handler(text="Главное меню", state=DialogueStates.GOT_ANSWER)
@dp.message_handler(text="Главное меню", state=DialogueStates.NO_NEW_QUESTIONS)
@dp.message_handler(text="Главное меню", state=DialogueStates.DO_NOT_UNDERSTAND_2)
async def back_to_main_menu(message: aiotypes.Message):
    """
    Возвращаемся в главное меню
    """
    view = views.get_main_menu()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await DialogueStates.MAIN_MENU.set()


@dp.message_handler(text="Готов!", state=DialogueStates.ANDROID_DEVELOPER_INIT_VIEW)
@dp.message_handler(text="Решить другую задачу", state=DialogueStates.GOT_ANSWER)
@dp.message_handler(text="Решить другую задачу", state=DialogueStates.DO_NOT_UNDERSTAND_2)
async def get_another_question(message: aiotypes.Message, state: FSMContext):
    """
    Выдать пользователю задачу
    """
    state_data = await state.get_data()

    view = views.get_next_question(message.from_user.id, state_data["answer_type"])

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await state.update_data(question_id=view.question_id)

    if view.question_id:
        await DialogueStates.ASK_QUESTION.set()
    else:
        await DialogueStates.NO_NEW_QUESTIONS.set()


@dp.message_handler(text="Далее", state=DialogueStates.ASK_QUESTION)
async def call_to_send_answer(message: aiotypes.Message, state: FSMContext):
    """
    Приглашаем написать ответ, если мысленно, то пусть просто нажмет ответил мысленно.
    """
    state_data = await state.get_data()

    view = views.get_call_to_send_answer(state_data["answer_type"])

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await DialogueStates.next()


@dp.message_handler(text="Не понял вопрос", state=DialogueStates.ASK_QUESTION)
async def do_not_understand_question(message: aiotypes.Message):
    """
    Если нажал кнопку "Не понял вопрос"
    """
    view = views.get_do_not_understand_question()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await DialogueStates.DO_NOT_UNDERSTAND_1.set()


@dp.message_handler(state=DialogueStates.DO_NOT_UNDERSTAND_1)
async def why_do_not_understand(message: aiotypes.Message):
    """
    Получили описание, почему вопрос не понятен
    """
    if message.text != "Отмена":
        pass  # TODO: записать что непонятного в вопросе

    view = views.get_why_do_not_understand()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await DialogueStates.next()


@dp.message_handler(
    content_types=[aiotypes.ContentType.TEXT, aiotypes.ContentType.VOICE],
    state=[DialogueStates.ASK_QUESTION, DialogueStates.CALL_TO_SEND_ANSWER],
)
async def get_answer(message: aiotypes.Message, state: FSMContext):
    """
    Читает ответ пользователя
    """
    state_data = await state.get_data()
    voice_id = None
    if message.text == "Ответил мысленно":
        answer_type = AnswerTypes.MENTAL.value
    elif message.content_type == aiotypes.ContentType.VOICE:
        answer_type = AnswerTypes.VOICE.value
        voice_id = message.voice.file_id
    elif message.content_type == aiotypes.ContentType.TEXT:
        answer_type = AnswerTypes.TEXT.value
    else:
        await message.reply("Такой ответ мы не принимаем! Напиши текстом, или продиктуй!")
        return

    answer = schemas.Answer(
        quest_id=state_data["question_id"],
        tg_user_id=message.from_user.id,
        answer_type=answer_type,
        text_answer=message.text,
        link_to_audio_answer=voice_id,
    )

    with Actions() as act:
        act.add_answer(answer)

    view = views.get_correct_answer(message.from_user.id)

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await DialogueStates.GOT_ANSWER.set()
