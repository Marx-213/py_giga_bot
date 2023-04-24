import logging
from http import HTTPStatus
from typing import Optional, Union

import requests
from config import code_to_smile, temp_to_smile


def get_current_weather(city: str, WEATHER_TOKEN: str) -> Union[int, dict]:
    '''Делает запрос к URL, возвращает json-файл.'''

    # Получаем ответ от API
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/'
        f'weather?q={city}&appid={WEATHER_TOKEN}&units=metric&lang=ru'
    )
    # Возвращаем json, если всё нормально. Или None, если нет
    if response.status_code != HTTPStatus.OK:
        logging.error(f'Сайт не доступен, код ответа {response.status_code}')
        return
    try:
        response = response.json()
        logging.info(f'Получен ответ: {response}')
        return response
    except Exception as error:
        logging.error(f'Произошла ошибка: {error}')
        raise Exception(f'Произошла ошибка: {error}')


def get_weather_message(data: str) -> Optional[str]:
    '''Принимает json-файл и возвращает сообщение с текущей погодой.'''

    # Получаем данные из json
    try:
        city = data['name']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        feels_like = data['main']['feels_like']
        wind = data['wind']['speed']
        weather = data['weather'][0]['description']
        weather_description = data['weather'][0]['main']
        # Преобразуем temp в смайлик
        temp_smile = temp_to_smile(temp)

    except Exception as error:
        logging.error(f'Проверьте название города. Ошибка: {error}')
        raise Exception(f'Произошла ошибка: {error}')
    # Преобразуем weather_description в смайлик
    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = ''
    # Формируем сообщение и возвращаем его
    weather_message = (
        f'Город: {city}, {wd}\nТемпература: {temp} C° {temp_smile}\n'
        f'Ощущается как {feels_like} C°{temp_smile}\n'
        f'Погода: {weather} \nВлажность: {humidity}% 💧\n'
        f'Ветер: {wind} м/с'
    )
    return weather_message
