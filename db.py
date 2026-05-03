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
    # Открываем подключение к базе данных и автоматически закрываем его после выхода из блока.
    async with aiosqlite.connect(DB_USERS_INCOME) as db:
        # Выполняем запрос: добавляем нового пользователя или обновляем доход существующего.
        await db.execute(
            """
            INSERT INTO DB_USERS_INCOME (user_id, income)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                income = excluded.income
            """,
            (user_id, income),
        )
        # Фиксируем изменения, чтобы доход точно сохранился в базе.
        await db.commit()


async def getting_user_salary(user_id):
    # Открываем подключение к базе данных для чтения сохраненного дохода.
    async with aiosqlite.connect(DB_USERS_INCOME) as db:
        # Выполняем SELECT-запрос: ищем income только для переданного user_id.
        cursor = await db.execute(
            """
            SELECT income FROM DB_USERS_INCOME 
            WHERE user_id = ?
            """,
            (user_id,)
        )
        # Забираем одну строку результата, потому что user_id уникальный.
        row = await cursor.fetchone()
        # Если строки нет, значит пользователь еще не сохранял доход.
        if row is None:
            return None
        else:
            # Возвращаем первый элемент строки: это колонка income.
            return row[0]
