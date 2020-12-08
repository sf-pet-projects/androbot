from aiogram import types as aiotypes
from aiogram.dispatcher import FSMContext

from . import schemas, states_, views
from .actions import Actions, start_new_test
from .errors import UserExistsException
from .main import bot, dp
from .specialty import Specialty
from .utils import Utils


@dp.message_handler(commands=["add_question"], state="*")
async def add_test_question(message):
    """
    Добавим новых тупых вопросов
    """
    question1 = schemas.Question(
        quest_id=Utils.get_random_number(5),
        question_type=Specialty.ANDROID.value,
        text_answer=Utils.get_random_text(10),
    )
    Actions().add_question(question1)
    await message.reply(question1)


@dp.message_handler(commands=["start"], state="*")
async def send_start_screen(message: aiotypes.Message):
    """
    Обработчик для команды start.
    """
    full_user_name = " ".join(
        [name for name in [message.from_user.first_name, message.from_user.last_name] if name]
    )
    tg_user = schemas.TelegramUser(
        tg_user_id=message.from_user.id,
        name=full_user_name,
        username=message.from_user.username,
        specialty="Android Developer",  # TODO это не должно быть обязательным полем
    )

    try:
        Actions().add_user(tg_user)
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

    await states_.DialogueStates.MAIN_MENU.set()


@dp.message_handler(text="Android Developer", state=states_.DialogueStates.MAIN_MENU)
async def show_android_developer_init(message: aiotypes.Message):
    """
    Обработчик для кнопки выбора специализации Android developer
    """
    view = views.get_android_developer_init_view()

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await states_.DialogueStates.next()


@dp.message_handler(text="Готов!", state=states_.DialogueStates.ANDROID_DEVELOPER_INIT_VIEW)
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

    await states_.DialogueStates.next()


@dp.message_handler(text="Отмена", state=states_.DialogueStates.ANDROID_DEVELOPER_INIT_VIEW)
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

    await states_.DialogueStates.MAIN_MENU.set()


@dp.message_handler(state=states_.DialogueStates.SELECT_ANSWER_TYPE)
async def show_first_question(message: aiotypes.Message, state: FSMContext):
    """
    Проверяем что-за вариант ответа он выбрал.
    Если ОК, задаем первый вопрос.
    """

    if message.text not in start_new_test():
        await message.reply("Ты выбрал некорректный вариант. Попробуй еще раз.", reply=False)
        return

    await state.update_data(answer_type=message.text)

    view = views.get_next_question(message.from_user.id)

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )

    await state.update_data(question_id=view.question_id)

    if view.question_id:
        await states_.DialogueStates.next()
    else:
        await state.finish()


@dp.message_handler(text="Далее", state=states_.DialogueStates.ASK_QUESTION)
async def call_to_send_answer(message: aiotypes.Message, state: FSMContext):
    """
    Приглашаем написать ответ, если мысленно, то пусть просто нажмет ответил мысленно.
    """
    await message.reply("Напиши ответ, или продиктуй его голосом.", reply=False)

    await states_.DialogueStates.next()


@dp.message_handler(text="Не понял вопрос", state=states_.DialogueStates.ASK_QUESTION)
async def do_not_understand_question(message: aiotypes.Message, state: FSMContext):
    """
    Если нажал кнопку "Не понял вопрос"
    """
    await message.reply("Ну не понял, так не понял.", reply=False)

    await state.finish()


@dp.message_handler(state=states_.DialogueStates.CALL_TO_SEND_ANSWER)
async def waiting_for_answer(message: aiotypes.Message, state: FSMContext):
    """
    Читает ответ пользователя
    """
    state_data = await state.get_data()

    await message.reply(f'Ты ответил {state_data["answer_type"]}!', reply=False)

    answer = schemas.Answer(
        quest_id=state_data["question_id"],
        tg_user_id=message.from_user.id,
        answer_type="text",
        text_answer=message.text,
        link_to_audio_answer="",
    )

    Actions().add_answer(answer)

    await message.reply("Правильный ответ 42", reply=False)

    await state.finish()
