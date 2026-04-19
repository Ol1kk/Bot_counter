# Импортируем асинхронную библиотеку для работы с SQLite.
import aiosqlite

# Константа с именем файла базы данных.
DB_USERS_INCOME = "bot.db"


# Асинхронная функция для создания базы/таблицы при запуске.
async def create_db():
    # Открываем подключение к базе данных и автоматически закрываем его после выхода из блока.
    async with aiosqlite.connect(DB_USERS_INCOME) as db:
        # Выполняем SQL-запрос на создание таблицы, если такой таблицы еще нет.
        await db.execute("""
        -- Создаем таблицу DB_USERS_INCOME только при ее отсутствии.
        CREATE TABLE IF NOT EXISTS DB_USERS_INCOME (
            -- Идентификатор пользователя Telegram, уникальный ключ.
            user_id INTEGER PRIMARY KEY,
            -- Сумма дохода пользователя.
            income INTEGER
        )
        """)
        # Фиксируем изменения в базе данных.
        await db.commit()


async def saving_income(user_id, income):
    async with aiosqlite.connect(DB_USERS_INCOME) as db:
        await db.execute(
            """
            INSERT INTO DB_USERS_INCOME (user_id, income)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                income = excluded.income
            """,
            (user_id, income),
        )
        await db.commit()
