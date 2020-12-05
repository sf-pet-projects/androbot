from aiogram import types as aiotypes

from . import actions, states, views
from .config import settings
from .errors import UserExistsException
from .main import bot, dp


@dp.message_handler(commands=["start"], state="*")
async def send_start_screen(message: aiotypes.Message):
    """
    Обработчик для команды start.

    Выполняет действия:
    1. Созадем пользователя в базе (если его еще нет)
    2. Регистрируем событие что пользователь нажал старт
    3. Формируем ответное сообщение и показываем главное меню
    """
    try:
        actions.Actions().add_user(message)

        view = views.get_hello_message(message)
        await bot.send_message(
            text=view.text,
            chat_id=message.chat.id,
            parse_mode=aiotypes.ParseMode.MARKDOWN,
            reply_markup=view.markup,
        )

    except UserExistsException:
        pass

    state = dp.current_state(user=message.from_user.id)
    await state.set_state("main_menu")

    view = views.get_main_menu(message)

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )


@dp.message_handler(text="Android Developer", state=states.DialogueStates.MAIN_MENU)
async def show_android_developer_init(message: aiotypes.Message):
    """
    Обработчик для кнопки выбора специализации Android developer
    """

    state = dp.current_state(user=message.from_user.id)
    await state.set_state("android_developer_init_view")

    view = views.get_android_developer_init_view(message)

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )


@dp.message_handler(text="Готов!", state=states.DialogueStates.ANDROID_DEVELOPER_INIT_VIEW)
async def show_select_answer_type(message: aiotypes.Message):
    """
    Предагаем выбрать вариант ответа
    """
    state = dp.current_state(user=message.from_user.id)
    await state.set_state("select_answer_type")

    view = views.get_select_answer_type_view(message)

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )


@dp.message_handler(text="Отмена", state=states.DialogueStates.ANDROID_DEVELOPER_INIT_VIEW)
async def back_to_main_menu(message: aiotypes.Message):
    """
    Возвращаемся в главное меню
    """

    state = dp.current_state(user=message.from_user.id)
    await state.set_state("main_menu")

    view = views.get_main_menu(message)

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )


@dp.message_handler(state=states.DialogueStates.SELECT_ANSWER_TYPE)
async def show_first_question(message: aiotypes.Message):
    """
    Зададем тестовый
    """

    if message.text.lower() not in [x.lower() for x in settings.answers_types.split(",")]:
        await message.reply("Ты выбрал некорректный вариант. Попробуй еще раз.", reply=False)
        return

    state = dp.current_state(user=message.from_user.id)
    await state.set_state("first_question")

    text_answer = "Ответьте на Главный вопрос жизни, Вселенной и всего такого."

    await bot.send_message(message.chat.id, text_answer)


@dp.message_handler(state=states.DialogueStates.FIRST_QUESTION)
async def check_first_question(message: aiotypes.Message):
    """
    Проверяем ответ на тестовый вопрос
    """
    user_answer = message.text

    if user_answer == "42":
        await message.reply("Да ты шаришь в теме")
        state = dp.current_state(user=message.from_user.id)
        await state.set_state("main_menu")

    else:
        await message.reply("Неверно, подумайте еще!", reply=False)
