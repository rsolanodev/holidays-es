import datetime

import pytest

from holidays_es import HolidaySpain, enums, exceptions, models


@pytest.fixture
def holiday_spain():
    return HolidaySpain(province=enums.Province.VALENCIA, year=2020)


def test_national_holidays(holiday_spain):
    expected_holiday = models.Holiday(
        scope=enums.Scope.NATIONAL,
        date=datetime.date(day=12, month=10, year=holiday_spain.year),
        description="Fiesta Nacional Española",
    )
    assert expected_holiday in holiday_spain.national

    for holiday in holiday_spain.national:
        assert holiday.scope == enums.Scope.NATIONAL


def test_regional_holidays(holiday_spain):
    expected_holiday = models.Holiday(
        scope=enums.Scope.REGIONAL,
        date=datetime.date(day=9, month=10, year=holiday_spain.year),
        description="Día de la Comunidad Valenciana",
    )
    assert expected_holiday in holiday_spain.regional

    for holiday in holiday_spain.regional:
        assert holiday.scope == enums.Scope.REGIONAL


def test_local_holidays(holiday_spain):
    expected_holiday = models.Holiday(
        scope=enums.Scope.LOCAL,
        date=datetime.date(day=20, month=4, year=holiday_spain.year),
        description="San Vicente Ferrer",
    )
    assert expected_holiday in holiday_spain.local

    for holiday in holiday_spain.local:
        assert holiday.scope == enums.Scope.LOCAL


def test_get_month_index_valid(holiday_spain):
    assert holiday_spain._get_month_index("Enero") == 1
    assert holiday_spain._get_month_index("Diciembre") == 12


def test_get_month_index_invalid(holiday_spain):
    with pytest.raises(ValueError):
        holiday_spain._get_month_index("Enro")


def test_province_invalid():
    with pytest.raises(exceptions.ProvinceError):
        HolidaySpain(province="valencia")


def test_year_below_minimum():
    with pytest.raises(exceptions.YearError):
        HolidaySpain(province=enums.Province.VALENCIA, year=2019, min_year=2020)


def test_year_above_maximum():
    with pytest.raises(exceptions.YearError):
        HolidaySpain(province=enums.Province.VALENCIA, year=2021, max_year=2020)


def test_find_holiday(holiday_spain):
    holiday_date = datetime.date(day=1, month=1, year=2020)
    expected_holiday = models.Holiday(
        scope=enums.Scope.NATIONAL,
        date=holiday_date,
        description="Año nuevo",
    )
    assert expected_holiday == holiday_spain.find(date=holiday_date)
