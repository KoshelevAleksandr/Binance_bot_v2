import os

from aiogram import Bot, Dispatcher, executor, types
import sql_db
from dotenv import find_dotenv, load_dotenv
from sql_db import BotDB


load_dotenv(find_dotenv())


async def on_startup(_):
    print('Бот вышел в онлайн')
    # sql_db.sql_start()

BotDB = BotDB('bot_db.db')
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)

    await bot.send_message(chat_id=message.chat.id, text='Добро пожаловать')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
