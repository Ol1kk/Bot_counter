# Импортируем модуль calendar, чтобы узнавать количество дней в месяце.
import calendar
# Импортируем date, чтобы получить сегодняшнюю дату.
from datetime import date


def calc_salary(income):
    # Получаем сегодняшнюю дату.
    today = date.today()
    # Берем номер текущего месяца из сегодняшней даты.
    month = today.month
    # Берем текущий год из сегодняшней даты.
    year = today.year
    # Получаем информацию о текущем месяце: день недели первого числа и количество дней.
    days_num = calendar.monthrange(year, month)
    # Берем второй элемент результата: количество дней в текущем месяце.
    days_num = days_num[1]
    # Делим месячный доход на количество дней и получаем доход за один день.
    todays_salary = income/days_num
    # Возвращаем рассчитанный дневной доход туда, где вызвали функцию.
    return todays_salary

def calc_day_salary(income, date):
    calc_date = date
    month = calc_date.month
    year = calc_date.year
    days_num = calendar.monthrange(year, month)
    # Берем второй элемент результата: количество дней в выбранном месяце.
    days_num = days_num[1]
    # Делим месячный доход на количество дней и получаем доход за один день.
    choose_day_salary = income/days_num
    # Возвращаем рассчитанный дневной доход туда, где вызвали функцию.
    return choose_day_salary
