# Импортируем Router для регистрации обработчиков сообщений.
from aiogram import Router
# Импортируем фильтр команды /start.
from aiogram.filters import CommandStart
# Импортируем тип Message для входящих сообщений Telegram.
from aiogram.types import Message
# Импортируем универсальный фильтр команд (например /get_date, /set_income).
from aiogram.filters import Command
# Импортируем базовый класс группы состояний FSM (сейчас в этом файле не используется напрямую).
from aiogram.fsm.state import StatesGroup
# Импортируем тип одного состояния FSM (сейчас в этом файле не используется напрямую).
from aiogram.fsm.state import State
# Импортируем контекст FSM для установки/сброса состояний пользователя.
from aiogram.fsm.context import FSMContext
# Импортируем нашу группу состояний Income из отдельного файла states.py.
from states import Income
from db import saving_income
from db import getting_user_salary
from calculations import calc_salary

# Создаем роутер, к которому привязываются все хэндлеры в этом файле.
router = Router()

# Регистрируем хэндлер: сработает, когда пользователь отправит команду /start.
@router.message(CommandStart())  # Фильтр для команды /start.
async def handler_start_message(msg):  # Асинхронный хэндлер команды /start.
    # Отправляем пользователю приветственное/стартовое сообщение.
    await msg.answer("Что вы хотите сделать?")


# Регистрируем хэндлер: сработает на команду /get_date.
@router.message(Command("get_date"))  # Фильтр для команды /get_date.
async def handler_date_message(date_question):  # Асинхронный хэндлер команды /get_date.
    # Отправляем пользователю сообщение с просьбой указать дату расчета зарплаты.
    await date_question.answer("Укажите дату расчета зарплаты")


# Регистрируем хэндлер: сработает на команду /set_income.
@router.message(Command("set_income"))  # Фильтр для команды /set_income.
async def handler_stub_message(msg, state):  # Асинхронный хэндлер начала ввода дохода.
    # Просим пользователя ввести сумму дохода за месяц.
    await msg.answer("Введите сумму дохода за месяц")
    # Переводим пользователя в состояние ожидания ввода дохода.
    await state.set_state(Income.waiting_for_income)


# Регистрируем хэндлер: сработает на любое сообщение, пока активное состояние Income.waiting_for_income.
@router.message(Income.waiting_for_income)  # Фильтр состояния ожидания дохода.
async def handler_income_message(msg, state):  # Асинхронный хэндлер обработки введенной суммы.
    # Начинаем блок обработки, который может выбросить ошибку ValueError при неверном вводе.
    try:
        # Берем текст сообщения пользователя и удаляем лишние пробелы по краям.
        user_text = msg.text.strip()
        # Преобразуем строку в число: заменяем запятую на точку и приводим к float.
        number = float(user_text.replace(",", "."))
        id_from_user = msg.from_user.id


        # Отправляем подтверждение, что доход принят, и показываем распознанное число.
        await saving_income(id_from_user, number)
        await msg.answer(f"Принято. Доход: {number}")
        # Сбрасываем состояние пользователя, завершая шаг ввода дохода.
        await state.clear()

    # Перехватываем ошибку, если введенное значение нельзя преобразовать в число.
    except ValueError:
        # Просим пользователя ввести корректное числовое значение.
        await msg.answer("Пожалуйста, введите число")


@router.message(Command("daily_salary"))
async def daily_salary_message(msg):
    get_id_from_user = msg.from_user.id
    salary = await getting_user_salary(get_id_from_user)
    if salary is None:
        await msg.answer("Сначала нужно задать зарплату командой /set_income")
    else:
        daily_salary = calc_salary(salary)
        await msg.answer(f"Доход на сегодня: {daily_salary}")
