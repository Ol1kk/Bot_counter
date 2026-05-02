import calendar
from datetime import date

def calc_salary(income):
    today = date.today()
    month = today.month
    year = today.year
    days_num = calendar.monthrange(year, month)
    days_num = days_num[1]
    todays_salary = income/days_num
    return todays_salary