from .main import dp

from dataclasses import *
from aiogram import types as aiotypes



@dp.message_handler(commands=["start", "help"])
async def send_welcome(


        message: aiotypes.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: aiotypes.Message):
    await message.answer(message.text)
