from aiogram import types as aiotypes

from . import crud
from .database import SessionLocal
from .errors import ErrorExample
from .main import dp
from .schemas import User, UserCreate


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: aiotypes.Message):
    """Этот хэндлер будет вызван при обращении к командам ``/start`` или ``/help``"""
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=["error"])
async def raise_error_example(message: aiotypes.Message):
    """При вызове команды /error в боте будет выдана демонстрация работы обработки ошибок"""
    raise ErrorExample("Error occurred intentionally", message)


@dp.message_handler(commands=["user"])
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


@dp.message_handler()
async def echo(message: aiotypes.Message):
    """Хэндлер просто отвечает сообщением, которое было прислоано"""
    await message.answer(message.text)
