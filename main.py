import asyncio
import logs
import sys
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Start its Telegram test Bot mirror all message")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
    logs.track(f"{message.from_user.id} Write: {message.text}")


if __name__ == '__main__':
    executor.start_polling(dp)
