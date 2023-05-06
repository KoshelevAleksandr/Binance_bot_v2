import os
import request_binance

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sql_db
from dotenv import find_dotenv, load_dotenv
from sql_db import BotDB

load_dotenv(find_dotenv())


async def on_startup(_):
    print('Бот вышел в онлайн')

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

BotDB = BotDB('bot_db.db')


class Form(StatesGroup):
    currency = State()


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    if message.text == '/help':
        await message.answer(text='Я бот для отслеживания цены BTC на Binance\nПо умолчания выбрана валюта usdt, которую можно изменить на eur или rub')
    else:
        await message.answer(text='Добро пожаловать')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.KeyboardButton('/Узнать_цену_BTC')
        b2 = types.KeyboardButton('/Изменить_валюту')
        b3 = types.KeyboardButton('/Задать_границы_уведомления')
        keyboard.row(b1, b2).row(b3)
        await message.answer(text='Выберете действие', reply_markup=keyboard)


@dp.message_handler(commands='Главное_меню')
async def main_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton('/Узнать_цену_BTC')
    b2 = types.KeyboardButton('/Изменить_валюту')
    b3 = types.KeyboardButton('/Задать_границы_уведомления')
    keyboard.row(b1, b2).row(b3)
    await message.answer(text='Выберете действие', reply_markup=keyboard)


@dp.message_handler(commands=['Узнать_цену_BTC'])
async def get_price(message: types.Message):
    currency = BotDB.get_currency(message.from_user.id)
    price = request_binance.currency_selection(currency)
    text_message = f'1 BTC = {str(price)} {currency}'
    await message.answer(text=text_message)


@dp.message_handler(commands=['Изменить_валюту'])
async def select_currency(message: types.Message):
    current_currency = BotDB.get_currency(message.from_user.id)
    await message.answer(text=f'Текущая валюта {current_currency}')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['usdt', 'eur', 'rub']
    b4 = types.KeyboardButton('/Главное_меню')
    keyboard.row(*buttons).row(b4)
    await message.answer(text='Выберете валюту в которой хотите получать цену BTC', reply_markup=keyboard)


@dp.message_handler(commands=['Задать_границы_уведомления'])
async def set_borders(message: types.Message):
    if BotDB.borders_exists(message.from_user.id):
        min_price = BotDB.get_borders(message.from_user.id)[0]
        max_price = BotDB.get_borders(message.from_user.id)[1]
    else:
        min_price = 'None'
        max_price = 'None'
    await message.answer(text=f'Текущие границы:\nmin_price = {min_price}\nmax_price = {max_price}')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton('/max_price')
    b2 = types.KeyboardButton('/min_price')
    b3 = types.KeyboardButton('/Главное_меню')
    keyboard.row(b1, b2).row(b3)
    await message.answer(text='Какую границу желаете изменить', reply_markup=keyboard)

@dp.message_handler(commands=['min_price'])
async def set_min_border(message: types.Message):
    BotDB.set_min_price(message.from_user.id, )


@dp.message_handler(commands=['max_price'])
async def set_min_border(message: types.Message):
    BotDB.set_max_price(message.from_user.id, )


@dp.message_handler(content_types=['text'])
async def save_currency(message: types.Message):
    currency = ['usdt', 'eur', 'rub']
    if message.text in currency:
        BotDB.update_currency(message.from_user.id, message.text)
        await message.answer(text=f'Основная валюта изменена на {message.text}')
        await main_menu(message)


@dp.message_handler()
async def default(message: types.Message):
    await message.answer(text='Команда не найдена')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
