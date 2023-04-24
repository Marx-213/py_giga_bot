# py_weather_bot

![Python](https://img.shields.io/badge/Python_3.7-14354C?style=for-the-badge&logo=python&logoColor=white)![React](https://img.shields.io/badge/pytelegrambotapi_4.6.1-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)![](https://img.shields.io/badge/SQLite-%23092E20?style=for-the-badge&logo=sqlite&logoColor=white)

### Описание
Погодный бот для социальной сети Telegram.
При нажатии команды /start бот сохраняет id юзера в БД с помошью sqlite3.

Бот имеет несколько хэндлеров а также кнопок с командами:
- Погода на сегодня
- Погода на завтра
- Погода на 3 дня

После выбора команды бот включает хэндлер для текстовых сообщений и ждет ввода от пользователя, который вводит название города. 
Бот с названием города обращается к OpenWeatherAPI, берет полученные данные, формирует ответ и отправляет его пользователю. Может отправлять геолокацию запрошенного города.
Есть своя система для рассылки сообщений юзерам, которые использовали команду /start.
Также есть функция для расчета правильного времени рассвета и заката, в зависимости от сервера, на котором стоит бот. 
### Установка
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/yandex-praktikum/py_weather_bot.git
```
Перейти в папку проекта:
``` 
cd
```
Установить и активировать виртуальное окружение:
``` 
python3 -m venv env
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
``` 
Создайте файл .env и заполните его данными:
```
TOKEN= <Токен вашего бота в telegram>
WEATHER_TOKEN= <Ваш токен на OpenWeatherApi>
```
### Технологии
- Python
- pyTelegramBotAPI
- sqlite3
