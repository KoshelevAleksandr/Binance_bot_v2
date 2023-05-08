import os
import request_binance

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

import sql_db
from dotenv import find_dotenv, load_dotenv
from sql_db import BotDB

load_dotenv(find_dotenv())


async def on_startup(_):
    print('Бот вышел в онлайн')

bot = Bot(token=os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

BotDB = BotDB('bot_db.db')


class Form(StatesGroup):
    min_price = State()
    max_price = State()


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
        b3 = types.KeyboardButton('/Границы_уведомления')
        keyboard.row(b1, b2).row(b3)
        await message.answer(text='Выберете действие', reply_markup=keyboard)


@dp.message_handler(commands='Главное_меню')
async def main_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton('/Узнать_цену_BTC')
    b2 = types.KeyboardButton('/Изменить_валюту')
    b3 = types.KeyboardButton('/Границы_уведомления')
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


@dp.message_handler(commands=['Границы_уведомления'])
async def set_borders(message: types.Message):
    if BotDB.borders_exists(message.from_user.id):
        min_price = BotDB.get_borders(message.from_user.id)[0]
        max_price = BotDB.get_borders(message.from_user.id)[1]
    else:
        min_price = 'None'
        max_price = 'None'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton('/Изменить_границы')
    b2 = types.KeyboardButton('/Главное_меню')
    keyboard.row(b1).row(b2)
    await message.answer(text=f'Текущие границы:\nmin_price = {min_price}\nmax_price = {max_price}', reply_markup=keyboard)


@dp.message_handler(commands=['Изменить_границы'])
async def set_borders(message: types.Message):
    await Form.min_price.set()
    await message.reply("Введите min_price или напиши /cancel")


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')
    await main_menu(message)


@dp.message_handler(state=Form.min_price)
async def set_min_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['min_price'] = message.text
    await Form.max_price.set()
    await message.reply("Введите max_price")


@dp.message_handler(state=Form.max_price)
async def set_max_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['max_price'] = message.text

        min_price = data['min_price']
        max_price = data['max_price']
        BotDB.set_min_price(message.from_user.id, min_price)
        BotDB.set_max_price(message.from_user.id, max_price)
        await message.answer(text=f'Новые границы:\nmin_price = {min_price}\nmax_price = {max_price}')
        await state.finish()
        await main_menu(message)


@dp.message_handler(content_types=['text'])
async def save_currency(message: types.Message):
    currency = ['usdt', 'eur', 'rub']
    if message.text in currency:
        BotDB.update_currency(message.from_user.id, message.text)
        await message.answer(text=f'Основная валюта изменена на {message.text}')
        await main_menu(message)
    else:
        await default(message)


# @dp.message_handler(content_types=['text'])
# async def save_currency(message: types.Message):
#     currency = ['usdt', 'eur', 'rub']
#     if message.text in currency:
#         BotDB.update_currency(message.from_user.id, message.text)
#         await message.answer(text=f'Основная валюта изменена на {message.text}')
#         await main_menu(message)
#     else:
#         await default(message)


@dp.message_handler()
async def default(message: types.Message):
    await message.answer(text='Команда не найдена')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
