from config import get_bot_token  # Получаем функцию, которая читает BOT_TOKEN из файла .env.
import asyncio  # Нужен для запуска асинхронной функции через asyncio.run(...).
from aiogram import Bot, Dispatcher  # Bot = связь с Telegram API, Dispatcher = обработка входящих сообщений.
from handlers import router 

TOKEN = get_bot_token()  # Считываем токен один раз при запуске программы.


async def main():  # Главная асинхронная функция, в которой запускается бот.
    if TOKEN is None:  # Проверяем, что в .env действительно есть BOT_TOKEN.
        raise ValueError("No token in .env (BOT_TOKEN is empty)")  # Останавливаем программу с понятной ошибкой.

    bot = Bot(token=TOKEN)  # Создаем объект бота для общения с Telegram.
    dp = Dispatcher()  # Создаем диспетчер, который распределяет входящие апдейты по хендлерам.
    dp.include_router(router)
    
    await dp.start_polling(bot)  # Запускаем polling: бот постоянно получает новые сообщения.


if __name__ == "__main__":  # Этот блок работает только при прямом запуске файла main.py.
    asyncio.run(main())  # Запускаем асинхронную функцию main() как точку входа в программу.
