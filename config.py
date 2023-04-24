# Словарь со смайликами температуры
temp_to_smile_dict = {
    'Heat': '\U0001F525',
    'Norm': '\U0001f321',
    'Cold': '\U00002744',
}
# Словарь со смайликами погоды
code_to_smile = {
    'Clear': 'Ясно \U00002600',
    'Clouds': 'Облачно \U00002601',
    'Rain': 'Дождь \U00002614',
    'Drizzle': 'Дождь \U00002614',
    'Thunderstorm': 'Гроза \U0001F329',
    'Snow': 'Снег \U0001F328',
    'Mist': 'Туман \U0001F32B'
}
# Кнопка назад
back_button = '/cancel'
# Приветственный текст
start_message_text = '''
Привет! Я - многофункциональный бот!
Я имею следующие функции:
Погода  ☀️ /weather
Конвертировать валюту 💵 /convert
Фото котиков 🐱 /photo
Создать опрос 📊 /create_poll
'''
# url от catAPI
catapi_url = 'https://api.thecatapi.com/v1/images/search'


def temp_to_smile(temp: str) -> str:
    '''Возвращает смайлик в зависимости от температуры'''
    if int(temp) >= 28:
        temp_smile = temp_to_smile_dict['Heat']
    elif 10 < int(temp) < 28:
        temp_smile = temp_to_smile_dict['Norm']
    else:
        temp_smile = temp_to_smile_dict['Cold']
    return temp_smile
