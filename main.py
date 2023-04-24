import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup
from config import back_button, start_message_text
from convert import get_convert_api, get_convert_message
from current_weather import get_current_weather, get_weather_message
from dotenv import load_dotenv
from random_photos import get_photo_url, get_random_photo


# Получаем TOKEN и WEATHER_TOKEN
load_dotenv()
TOKEN = os.getenv('TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
# Создаем настройки для логирования
logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)
# Создаеи диспетчер
storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
# Добавляем кнопку /cancel, для  сброса состояния
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(back_button)


class WeatherForm(StatesGroup):
    '''Состояние для погоды с переменной city'''
    city = State()  # Город пользователя


class ConvertForm(StatesGroup):
    '''Состояние для конвертации с переменной convert_text'''
    convert_text = State()  # Текст с данными для конвертации


class PollForm(StatesGroup):
    '''Состояние для опросов '''
    chat_id = State()  # id группового чата
    question = State()  # вопрос опроса
    options = State()  # варианты ответа опроса


@dp.message_handler(commands=['start'])
async def start(message: types.Message) -> None:
    '''Запускается, когда юзер включает бота командой /start.
    Отправляет ему сообщение с приветствием.
    '''

    await message.answer(start_message_text)


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    '''Обработчик команды /cancel'''
    # Получаем текущее состояние
    current_state = await state.get_state()
    # Если состояние не существует, то просто отправляем start_message
    if current_state is None:
        await message.answer(start_message_text)
    # Если состояние существует, то удаляем его
    await state.finish()
    await message.answer(start_message_text)


@dp.message_handler(Command('weather'), state=None)
async def weather_handler(message: types.Message) -> None:
    '''Обработчик команды /weather, ждет название города,
    чтобы отправить его в weather_state
    '''

    await message.answer(
        'Введите город, чтобы получить погоду.',
        reply_markup=keyboard
    )
    # Переходим в WeatherForm
    await WeatherForm.city.set()


@dp.message_handler(state=WeatherForm.city)
async def weather_state(message: types.Message) -> None:
    '''Функция-обработчик состояния для команды /weather'''
    city = message.text
    # Получаем ответ от OpenWeatherAPI
    response = get_current_weather(city, WEATHER_TOKEN)
    if response is None:
        await message.answer(
            'Город не найден, попробуйте еще раз',
            reply_markup=keyboard
        )
    # Получаем данные о погоде
    weather = get_weather_message(response)
    # Отправляем ответ пользователю
    await message.answer(weather, reply_markup=keyboard)


@dp.message_handler(Command('convert'), state=None)
async def convert_handler(message: types.Message) -> None:
    '''Обработчик команды /convert, ждет текст с информацией для конвертации,
    чтобы отправить его в convert_state
    '''

    await message.answer(
        'Пожалуйста, введите две валюты для конвертации и количество, '
        'разделив их пробелом.\nНапример: usd rub 100.',
        reply_markup=keyboard
    )
    # Переходим в ConvertForm
    await ConvertForm.convert_text.set()


@dp.message_handler(state=ConvertForm.convert_text)
async def convert_state(message: types.Message) -> None:
    '''Функция-обработчик состояния для команды /convert'''
    # Из введенного текста получаем три переменные
    text = message.text
    try:
        currency_from, currency_to, amount = text.strip().upper().split()
    except ValueError:
        await message.reply(
            'Пожалуйста, убедитесь, что ввели две валюты для конвертации и '
            'количество, разделив их пробелом.', reply_markup=keyboard)
        return
    # Получаем ответ от API
    response = get_convert_api(currency_from, currency_to, amount)
    # Проверяем успешность запроса
    if response is None:
        await message.reply(
            'Ошибка при получении курса валют. Попробуйте позже.',
            reply_markup=keyboard
        )
        return
    # Получаем данные о курсе
    conversion_message = get_convert_message(response, currency_to)
    if conversion_message is None:
        await message.reply(
            'Ошибка при получении курса валют. Попробуйте позже.',
            reply_markup=keyboard
        )
        return
    # Отправляем ответ пользователю
    await message.answer(conversion_message, reply_markup=keyboard)


@dp.message_handler(Command('photo'), state=None)
async def photo_handler(message: types.Message) -> None:
    '''Обработчик команды /photo, делает запрос к API,
    и отправляет фотку юзеру
    '''

    # Получаем ответ от API в виде фотки
    response = get_random_photo()
    if response is None:
        await message.reply(
            'Ошибка при получении фотки котика. Попробуйте позже.'
        )
    photo = get_photo_url(response)
    # Отправляем фотку пользователю
    await message.answer_photo(photo, reply_markup=keyboard)


@dp.message_handler(Command('create_poll'), state=None)
async def start_poll(message: types.Message) -> None:
    '''Обработчик команды /create_poll, просит юзера написать chat_id группы'''

    # Отправляем пользователю сообщение с просьбой задать вопрос
    await message.answer('Введите chat_id для опроса:', reply_markup=keyboard)
    # Устанавливаем состояние в 'chat_id'
    await PollForm.chat_id.set()


@dp.message_handler(state=PollForm.chat_id)
async def save_chat_id(message: types.Message, state: FSMContext) -> None:
    '''Функция, которая сохраняет chat_id, и просит юзера написать вопрос'''

    # Сохраняем вопрос в состояние FSM
    await state.update_data(chat_id=message.text)
    await message.answer('Введите вопрос для опроса:', reply_markup=keyboard)
    # Устанавливаем состояние в 'question'
    await PollForm.question.set()


@dp.message_handler(state=PollForm.question)
async def save_question(message: types.Message, state: FSMContext) -> None:
    '''Функция, которая сохраняет вопрос в состояние FSM
    и спрашивает о вариантах ответа
    '''

    # Сохраняем вопрос в состояние FSM
    await state.update_data(question=message.text)
    # Приглашаем ввести варианты ответов
    await message.answer(
        'Введите варианты ответов для опроса, через запятую:',
        reply_markup=keyboard
    )
    # Устанавливаем состояние в 'options'
    await PollForm.options.set()


@dp.message_handler(state=PollForm.options)
async def add_options(message: types.Message, state: FSMContext) -> None:
    '''Функция, которая добавляет варианты ответа в опрос, и создает его'''

    # Получаем список вариантов ответа от пользователя
    options = message.text.split(',')
    # Сохраняем список вариантов ответа в состояние FSM
    await state.update_data(options=options)
    # Получаем введенные данные из state
    async with state.proxy() as data:
        chat_id = data['chat_id']
        question = data['question']
        options = data['options']
    # Отправляем опрос в групповой чат
    await bot.send_poll(chat_id=chat_id, options=options, question=question)
    # Сбрасываем состояние
    await state.finish()


def main() -> None:
    '''Главная функция.'''
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
