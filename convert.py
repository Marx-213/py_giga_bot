import logging
import os
from http import HTTPStatus
from typing import Optional, Union

import requests
from dotenv import load_dotenv

# Получаем CONVERT_API_KEY
load_dotenv()
CONVERT_API_KEY = os.getenv('CONVERT_API_KEY')


def get_convert_api(
        currency_from: str,
        currency_to: str,
        amount: str) -> Union[int, dict]:
    '''Делает запрос к exchangerateAPI, возвращает json-файл.'''

    # Получаем ответ от API
    response = requests.get(
        f'https://v6.exchangerate-api.com/v6/{CONVERT_API_KEY}/pair'
        f'/{currency_from}/{currency_to}/{amount}'
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


def get_convert_message(data: dict, currency_to: str) -> Optional[str]:
    '''Принимает json-файл и возвращает сообщение с результатом конвертации.'''

    # Получаем данные из json
    try:
        conversion_rate = data['conversion_rate']
        conversion_result = data['conversion_result']
    except Exception as error:
        logging.error(f'Ошибка: {error}')
        return
    # Формируем сообщение и возвращаем его
    conversion_message = (
        f'Курс 1 к {conversion_rate}.\n'
        f'Результат: {conversion_result} {currency_to}'
    )
    return conversion_message
