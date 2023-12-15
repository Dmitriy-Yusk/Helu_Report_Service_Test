from datetime import date, datetime
import src.utils as utils


def test_get_first_day_of_the_month():
    init_year = 2020
    init_month = 6
    init_value = date(year=init_year, month=init_month, day=15)

    value = utils.get_first_day_of_the_month(init_value)

    example_value = datetime(year=init_year, month=init_month, day=1)

    eq = value == example_value
    assert eq


def test_get_last_day_of_the_month():
    init_year = 2020
    init_month = 6
    init_value = date(year=init_year, month=init_month, day=15)

    value = utils.get_last_day_of_the_month(init_value)

    example_value = datetime.combine(date(year=init_year, month=init_month, day=30), datetime.max.time())

    eq = value == example_value
    assert eq


def test_get_month_name():
    date_val = date(year=2020, month=6, day=1)
    month_name = utils.get_month_name(date_val)

    eq = month_name == 'June'
    assert eq
