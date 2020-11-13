import logging

from aiogram import Bot, Dispatcher, executor
from loguru import logger
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    tg_api_token: str = Field(..., env="TG_API_TOKEN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


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
settings = Settings()
bot = Bot(token=settings.tg_api_token)
dp = Dispatcher(bot)


def main(dispatcher: Dispatcher):
    executor.start_polling(dispatcher, skip_updates=True)
