from dataclasses import dataclass
from datetime import date

from holidays_es.scopes import Scope



@dataclass(frozen=True, kw_only=True)
class Holiday:
    scope: Scope
    date: date
    description: str
