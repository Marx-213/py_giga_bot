import logging
from http import HTTPStatus
from typing import List, Optional, Union

import requests
from config import catapi_url


def get_random_photo() -> Union[int, dict]:
    '''Делает запрос к catAPI, возвращает json-файл.'''

    # Получаем ответ от API
    response = requests.get(catapi_url)
    # Возвращаем json, если всё нормально
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


def get_photo_url(data: List[dict]) -> Optional[str]:
    '''Принимает json-файл и возвращает url адрес фотки.'''

    try:
        photo_url = data[0]['url']
    except Exception as error:
        logging.error(f'Ошибка: {error}')
        raise Exception(f'Произошла ошибка: {error}')
    return photo_url
