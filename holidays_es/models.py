import datetime

import attr

from holidays_es import enums


@attr.define
class Holiday:
    scope: enums.Scope
    date: datetime.date
    description: str
