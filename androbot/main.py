import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from loguru import logger

from . import models
from .config import settings
from .database import engine

models.Base.metadata.create_all(bind=engine)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=0)

# Initialize bot and dispatcher
bot = Bot(token=settings.tg_api_token)

if settings.fsm_redis_host:
    storage = RedisStorage2(
        settings.fsm_redis_host,
        settings.fsm_redis_port,
        settings.fsm_redis_db,
        settings.fsm_redis_password,
    )
else:
    storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)


def main(dispatcher: Dispatcher):
    executor.start_polling(dispatcher, skip_updates=True)
