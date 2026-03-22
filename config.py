# config.py

from dotenv import load_dotenv  # Импортируем функцию load_dotenv из библиотеки python-dotenv, чтобы читать файл .env
import os  # Импортируем встроенный модуль os для работы с переменными окружения (например BOT_TOKEN)

def get_bot_token():  # Объявляем функцию get_bot_token, которая будет возвращать токен бота
    load_dotenv()  # Загружаем переменные из файла .env в окружение программы
    return os.getenv("BOT_TOKEN")  # Возвращаем значение переменной BOT_TOKEN (или None, если ее нет)
