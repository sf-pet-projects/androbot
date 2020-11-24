from aiogram import types as aiotypes

from . import backend, crud, states, views
from .database import SessionLocal
from .errors import ErrorExample
from .main import bot, dp
from .schemas import User, UserCreate


@dp.message_handler(commands=["start"], state="*")
async def send_start_screen(message: aiotypes.Message):
    """
    Обработчик для команды start.

    Выполняет действия:
    1. Созадем пользователя в базе (если его еще нет)
    2. Регистрируем событие что пользователь нажал старт
    3. Формируем ответное сообщение и показываем главное меню
    """
    backend.add_user(message.from_user)
    backend.register_action("start", message)

    state = dp.current_state(user=message.from_user.id)
    await state.set_state("main_menu")

    view = views.get_main_menu(message)

    await bot.send_message(
        text=view.text,
        chat_id=message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )


@dp.callback_query_handler(
    lambda c: c.data == "main_menu", state=states.MainDialogueStates.IN_PROFILE
)
async def callback_show_main_menu(callback_query: aiotypes.callback_query):
    """
    Обработчик для inline кнопки "Главное меню"
    """
    await bot.answer_callback_query(callback_query.id)

    await bot.edit_message_reply_markup(
        callback_query.message.chat.id,
        callback_query.message.message_id,
        callback_query.inline_message_id,
    )

    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state("main_menu")

    view = views.get_main_menu(callback_query)

    await bot.send_message(
        text=view.text,
        chat_id=callback_query.message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )


@dp.callback_query_handler(
    lambda c: c.data == "open_profile", state=states.MainDialogueStates.MAIN_MENU
)
async def callback_show_profile(callback_query: aiotypes.callback_query):
    """
    Обработчик для inline кнопки "Профиль"
    """
    await bot.answer_callback_query(callback_query.id)

    await bot.edit_message_reply_markup(
        callback_query.message.chat.id,
        callback_query.message.message_id,
        callback_query.inline_message_id,
    )

    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state("in_profile")

    view = views.get_profile(callback_query)

    await bot.send_message(
        text=view.text,
        chat_id=callback_query.message.chat.id,
        parse_mode=aiotypes.ParseMode.MARKDOWN,
        reply_markup=view.markup,
    )


@dp.callback_query_handler(
    lambda c: c.data == "android_developer", state=states.MainDialogueStates.MAIN_MENU
)
async def callback_first_question(callback_query: aiotypes.callback_query):
    """
    Обработчик для inline кнопки начала тестирования по направлению android
    Начинаем тестирование
    """
    await bot.answer_callback_query(callback_query.id)

    await bot.edit_message_reply_markup(
        callback_query.message.chat.id,
        callback_query.message.message_id,
        callback_query.inline_message_id,
    )

    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state("first_question")

    text_answer = "Ответьте на Главный вопрос жизни, Вселенной и всего такого."

    await bot.send_message(callback_query.message.chat.id, text_answer)


@dp.message_handler(commands=["help"], state="*")
async def send_welcome(message: aiotypes.Message):
    """Этот хэндлер будет вызван при обращении к команде ``/help``"""
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=["error"], state="*")
async def raise_error_example(message: aiotypes.Message):
    """При вызове команды /error в боте будет выдана демонстрация работы обработки ошибок"""
    raise ErrorExample("Error occurred intentionally", message)


@dp.message_handler(commands=["user"], state="*")
async def create_user(message: aiotypes.Message):
    user = UserCreate(email="rst", password="rstrst")
    db = SessionLocal()
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        crud.create_user(db=db, user=user)
        db_user = crud.get_user_by_email(db, email=user.email)
    user_json = User.from_orm(db_user).json()
    db.close()
    return await message.answer(user_json)


@dp.message_handler(state="*")
async def echo(message: aiotypes.Message):
    """Хэндлер просто отвечает сообщением, которое было прислано"""
    await message.answer(message.text)
