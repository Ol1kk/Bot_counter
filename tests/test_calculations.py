# Здесь будут автотесты для функций из calculations.py.
# Первый учебный тест можно написать для calc_day_salary.
from datetime import date
import calendar
import calculations
from calculations import calc_day_salary
from calculations import calc_salary
from unittest.mock import Mock, AsyncMock
import pytest
import db

def test_calc_day_salary_for_march():
    result = calc_day_salary(31000, date(2026, 3, 10))

    assert result == 1000

def test_calc_day_salary_for_leap_year():
    result = calc_day_salary(29000, date(2028, 2, 29))

    assert result == 1000

def test_calc_salary():
    today = date.today()
    days_in_month = calendar.monthrange(today.year, today.month)[1]

    result = calc_salary(31000)

    assert result == 31000/days_in_month

@pytest.mark.asyncio
async def test_save_and_get_user_income(tmp_path, monkeypatch):
    test_db = tmp_path / "test_bot.db"
    monkeypatch.setattr(db, "DB_USERS_INCOME", test_db)

    await db.create_db()
    await db.saving_income(user_id=123, income=50000)

    result = await db.getting_user_salary(user_id=123)

    assert result == 50000

@pytest.mark.asyncio
async def test_user_doesnt_exist(tmp_path, monkeypatch):
    test_db = tmp_path / "test_bot.db"
    monkeypatch.setattr(db, "DB_USERS_INCOME", test_db)

    await db.create_db()

    result = await db.getting_user_salary(user_id=999)

    assert result == None

@pytest.mark.asyncio
async def test_update_salary(tmp_path, monkeypatch):
    test_db = tmp_path / "test_bot.db"
    monkeypatch.setattr(db, "DB_USERS_INCOME", test_db)

    await db.create_db()

    result = await db.getting_user_salary(user_id=999)

    assert result == None

