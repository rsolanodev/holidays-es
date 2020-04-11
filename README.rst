Holidays ES
===========
A small Python package to obtain the public holidays in Spain from 2006 to the current year.
This application uses the web scraping technique to obtain the data from `calendarioslaborales.net <https://www.calendarioslaborales.com/>`_

Installation
------------
::

    pip install holidays-es

Usage
-----

We can get a list of all available provinces, **which include some municipalities**.
Once we have the name we can create our province object to obtain the holidays.

.. code-block:: python

    from holidays_es import get_provinces, Province

    provinces = get_provinces()
    print(provinces)

This code returns in a list all the available provinces.

::

    >>> python app.py
    ['alava', 'albacete', 'alicante', 'almeria', 'asturias', 'avila', 'badajoz', 'baleares', 'barcelona', 'bilbao', 'burgos', 'caceres', 'cadiz', 'cantabria', 'castellon', 'ceuta', 'ciudad-real', 'cordoba', 'la-coruna', 'cuenca', 'gijon', 'girona', 'granada', 'guadalajara', 'guipuzcoa', 'huelva', 'huesca', 'jaen', 'leon', 'lleida', 'logrono', 'lugo', 'madrid', 'malaga', 'melilla', 'murcia', 'navarra', 'ourense', 'oviedo', 'palencia', 'palma-de-mallorca', 'las-palmas', 'pamplona', 'pontevedra', 'la-rioja', 'salamanca', 'san-sebastian', 'santander', 'segovia', 'sevilla', 'soria', 'tarragona', 'tenerife', 'teruel', 'toledo', 'valencia', 'valladolid', 'vitoria', 'vizcaya', 'zamora', 'zaragoza']


With the names that we have available we can find out the holidays. We must indicate a
name to the Province object and the year if not indicated will use the current year.

.. code-block:: python

    from holidays_es import Province

    holidays = Province(name="valencia", year=2018).holidays()
    print(holidays)

This code returns in a dictionary the types of holidays in Spain with the dates.

::

    >>> python app.py
    {
        'national_holidays': [datetime.date(2018, 1, 1), datetime.date(2018, 1, 6), datetime.date(2018, 3, 30), datetime.date(2018, 5, 1), datetime.date(2018, 8, 15), datetime.date(2018, 10, 12), datetime.date(2018, 11, 1), datetime.date(2018, 12, 6), datetime.date(2018, 12, 8), datetime.date(2018, 12, 25)],
        'regional_holidays': [datetime.date(2018, 3, 19), datetime.date(2018, 4, 2), datetime.date(2018, 10, 9)],
        'local_holidays': [datetime.date(2018, 1, 22), datetime.date(2018, 4, 9)]
    }

We can also directly obtain national, regional or local holidays. And it will return the result in a list

.. code-block:: python

    from holidays_es import Province

    Province(name="valencia").national_holidays()
    Province(name="barcelona").regional_holidays()
    Province(name="madrid").local_holidays()


