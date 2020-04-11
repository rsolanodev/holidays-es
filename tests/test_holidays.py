import datetime

from holidays_es import get_provinces, Province


def test_provinces_count():
    """
    In the list of provinces you will also find municipalities,
    this is by https://www.calendarioslaborales.com/.
    """
    provinces = get_provinces()
    assert len(provinces) == 61


def test_types_holidays():
    """we have national, regional and local festivals."""
    holidays = Province(name="valencia").holidays()
    assert len(holidays) == 3


def test_national_holidays():
    """All the provinces have the same national holidays..."""
    valencia = Province(name="valencia").national_holidays()
    barcelona = Province(name="barcelona").national_holidays()
    assert len(valencia) == len(barcelona)


def test_regional_holidays():
    """In Valencia we have several regional festivals."""
    valencia = Province(name="valencia").regional_holidays()
    assert len(valencia) > 0


def test_local_holidays_and_current_year():
    """If we don't specify a year it will choose the current year."""
    valencia = Province(name="valencia").local_holidays()
    current_year = datetime.datetime.now().year
    assert valencia[0].year == current_year


def test_year_holidays():
    """Check that you can filter for holidays since 2016."""
    for year in range(2016, 2020):
        valencia = Province(name="valencia", year=year).national_holidays()
        assert valencia[0].year == year
