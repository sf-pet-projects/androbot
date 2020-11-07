from aiogram import types as aiotypes

from .main import dp


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: aiotypes.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: aiotypes.Message):
    await message.answer(message.text)
