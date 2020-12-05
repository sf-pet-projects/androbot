from aiogram import types as aiotypes
from loguru import logger

from androbot.errors import BaseAppError
from androbot.main import dp


@dp.errors_handler(exception=BaseAppError)
async def handle_app_error(update: aiotypes.Update, exception: BaseAppError) -> bool:
    if isinstance(exception, BaseAppError):
        logger.error("Unexpected error occurred {}", exception)
    await update.message.answer(exception.response)
    return True
