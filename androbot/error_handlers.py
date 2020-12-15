from aiogram import types as aiotypes
from loguru import logger

from androbot.main import dp


@dp.errors_handler()
async def handle_app_error(update: aiotypes.Update, exception: Exception):
    logger.error("Unexpected error occurred {}", repr(exception))
    await update.message.answer(
        f"На сервере произошла ошибка {repr(exception)}. "
        "Мы уже знаем и работает над её испавлением"
    )
