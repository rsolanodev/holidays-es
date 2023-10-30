===========
Holidays ES
===========

A small Python package to obtain the public holidays in Spain from 2006 to the current year.
This application uses the web scraping technique to obtain the data from
`calendarioslaborales.net <https://www.calendarioslaborales.com/>`_

Made with Python with ❤️

:Package:
    .. image:: https://img.shields.io/pypi/pyversions/holidays-es.svg?logo=python&label=Python&logoColor=gold
        :target: https://pypi.python.org/pypi/holidays-es
        :alt: Python supported versions

    .. image:: http://img.shields.io/pypi/v/holidays-es.svg?logo=pypi&label=PyPI&logoColor=gold
        :target: https://pypi.python.org/pypi/holidays-es
        :alt: PyPI version

    .. image:: https://img.shields.io/pypi/dm/holidays-es.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold
        :target: https://pypi.python.org/pypi/holidays-es
        :alt: Downloads

:CI/CD:
    .. image:: https://github.com/vacanza/python-holidays-es/workflows/CI%2FCD/badge.svg
        :target: actions

:Meta:
    .. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :alt: Code style

    .. image:: http://img.shields.io/pypi/l/holidays-es.svg
        :target: LICENSE
        :alt: License

Install
-------
Install via pip:

.. code-block:: shell

    $ pip install holidays-es

Quick Start
-----------
1.  Import the HolidaySpain class and set the province and year of the holidays you want to obtain.

.. code-block:: python

    from datetime import date
    from holidays_es import Province, HolidaySpain, Scope

    holiday_spain = HolidaySpain(province=Province.VALENCIA, year=2022)

    holiday_date = date(day=1, month=1, year=2022)
    expected_holiday = models.Holiday(
        scope=Scope.NATIONAL,
        date=holiday_date,
        description="Año nuevo",
    )

    assert expected_holiday == holiday_spain.find(date=holiday_date)


2. If you only need the national, regional, or local holidays, you can also obtain them in the following way:

.. code-block:: python

    from holidays_es import Province, HolidaySpain

    holiday_spain = HolidaySpain(province=Province.MADRID, year=2020)

    for holiday in holiday_spain.national:
        holiday.scope  # <Scope.NATIONAL: 'national'>
        holiday.date  # datetime.date(2023, 1, 1)
        holiday.description  # Año nuevo
