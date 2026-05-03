# Импортируем Router для регистрации обработчиков сообщений.
from aiogram import Router, F
# Импортируем фильтр команды /start.
from aiogram.filters import CommandStart
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
# Импортируем функцию сохранения дохода пользователя в базу.
from db import saving_income
# Импортируем функцию получения сохраненного дохода пользователя из базы.
from db import getting_user_salary
# Импортируем функцию расчета дневного дохода.
from calculations import calc_salary, calc_day_salary
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime




# Создаем роутер, к которому привязываются все хэндлеры в этом файле.
router = Router()
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Указать доход")],
        [KeyboardButton(text="Выбрать дату")],
        [KeyboardButton(text="Узнать доход за день")],
    ],
    resize_keyboard=True,
)

# Регистрируем хэндлер: сработает, когда пользователь отправит команду /start.
@router.message(CommandStart())  # Фильтр для команды /start.
async def handler_start_message(msg):  # Асинхронный хэндлер команды /start.
    # Отправляем пользователю приветственное/стартовое сообщение.
    await msg.answer("Что вы хотите сделать?", reply_markup=keyboard)


# Регистрируем хэндлер: сработает на команду /get_date.
@router.message(Command("get_date"))  # Фильтр для команды /get_date.
@router.message(F.text == "Выбрать дату")  # Фильтр для кнопки "Выбрать дату".
async def get_date_message(date_question, state):  # Асинхронный хэндлер команды /get_date.
    # Отправляем пользователю сообщение с просьбой указать дату расчета зарплаты.
    await date_question.answer("Укажите дату расчета зарплаты в формате ДД.ММ.ГГГГ")
    await state.set_state(Income.waiting_for_date)

@router.message(Income.waiting_for_date) 
async def handler_date_message(msg, state):
    try:
        user_text = msg.text.strip()
        selected_date = datetime.strptime(user_text, "%d.%m.%Y").date()
        
        get_id_from_user = msg.from_user.id
        salary = await getting_user_salary(get_id_from_user)
        # Проверяем, есть ли доход в базе: None означает, что пользователь еще не вводил сумму.
        if salary is None:
            # Просим пользователя сначала задать месячный доход.
            await msg.answer("Сначала нужно задать зарплату командой /set_income")
            await state.clear()
        else:
            # Считаем доход за один день на основе сохраненного месячного дохода.
            daily_salary = calc_day_salary(salary, selected_date)
            # Отправляем пользователю результат расчета.
            await msg.answer(f"Доход на {selected_date}: {daily_salary}")
            await state.clear()
    
    except ValueError:
        # Просим пользователя ввести корректное числовое значение.
        await msg.answer("Пожалуйста, введите корректную дату")


# Регистрируем хэндлер: сработает на команду /set_income.
@router.message(Command("set_income"))  # Фильтр для команды /set_income.
@router.message(F.text == "Указать доход")  # Фильтр для кнопки "Указать доход".
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
        # Получаем Telegram ID пользователя, чтобы сохранить доход именно для него.
        id_from_user = msg.from_user.id


        # Сохраняем доход пользователя в базу данных.
        await saving_income(id_from_user, number)
        # Отправляем подтверждение, что доход принят, и показываем распознанное число.
        await msg.answer(f"Принято. Доход: {number}")
        # Сбрасываем состояние пользователя, завершая шаг ввода дохода.
        await state.clear()

    # Перехватываем ошибку, если введенное значение нельзя преобразовать в число.
    except ValueError:
        # Просим пользователя ввести корректное числовое значение.
        await msg.answer("Пожалуйста, введите число")


@router.message(Command("daily_salary"))
@router.message(F.text == "Узнать доход за день")
async def daily_salary_message(msg):
    # Получаем Telegram ID пользователя, который запросил расчет дневного дохода.
    get_id_from_user = msg.from_user.id
    # Достаем сохраненный месячный доход пользователя из базы.
    salary = await getting_user_salary(get_id_from_user)
    # Проверяем, есть ли доход в базе: None означает, что пользователь еще не вводил сумму.
    if salary is None:
        # Просим пользователя сначала задать месячный доход.
        await msg.answer("Сначала нужно задать зарплату командой /set_income")
    else:
        # Считаем доход за один день на основе сохраненного месячного дохода.
        daily_salary = calc_salary(salary)
        # Отправляем пользователю результат расчета.
        await msg.answer(f"Доход на сегодня: {daily_salary}")
