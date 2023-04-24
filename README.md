# py_giga_bot

![Python](https://img.shields.io/badge/Python_3.7-14354C?style=for-the-badge&logo=python&logoColor=white)![Python](https://img.shields.io/badge/aiogram_2.25.1-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

### Описание
Многофункциональный бот для социальной сети Telegram.
При нажатии команды /start бот отправляет приветственное сообщение пользователю.

Бот имеет несколько функций:
- /weather - Получить погоду в определенном городе
- /convert - Конвертировать валюту
- /photo - Получить фото котика
- /create_poll - Создать опрос

### Установка
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/yandex-praktikum/py_giga_bot.git
``` 
Перейти в папку проекта:
``` 
cd py_giga_bot
```
Установить и активировать виртуальное окружение:
``` 
python3 -m venv venv
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
``` 
Создайть файл .env и заполните его данными:
```
TOKEN= <Токен вашего бота в telegram>
WEATHER_TOKEN= <Ваш токен на OpenWeatherApi>
CONVERT_API_KEY= <Ваш токен на ExchangeRatesAPI>
```
Запустите бота:
```
python main.py
```
### Технологии
- Python
- pyTelegramBotAPI
