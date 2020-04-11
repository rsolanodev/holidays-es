import datetime

import requests
from bs4 import BeautifulSoup

base = "https://www.calendarioslaborales.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 "
}


def get_provinces() -> list:
    page = requests.get(base, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    provinces = soup.findAll(
        "a", title=lambda value: value and value.startswith("Calendario laboral")
    )
    result = []
    for province in provinces:
        calendar = province.get("href").split("/")[-1].split(".")[0].split("-")[2:]
        calendar.pop()
        result.append("-".join(calendar))
    return result


class Province:
    def __init__(self, name, year=None):
        self.name = name
        self.year = datetime.datetime.now().year if year is None else year
        self._page = requests.get(
            f"{base}calendario-laboral-{name}-{self.year}.htm", headers=headers
        )
        self._soup = BeautifulSoup(self._page.content, "html.parser")

    def __tour_months(self, holiday):
        result = []
        for m in months():
            table_id = f"mes{m.title()}"
            table = self._soup.find(id=table_id)
            holidays = table.findAll("td", {"class": f"cajaFestivo{holiday}"})
            for h in holidays:
                day = int(h.get_text())
                month = months().index(m) + 1
                date = datetime.date(day=day, month=month, year=self.year)
                result.append(date)
        return result

    def national_holidays(self) -> list:
        return self.__tour_months("N")

    def regional_holidays(self) -> list:
        return self.__tour_months("R")

    def local_holidays(self) -> list:
        return self.__tour_months("P")

    def holidays(self):
        return {
            "national_holidays": self.national_holidays(),
            "regional_holidays": self.regional_holidays(),
            "local_holidays": self.local_holidays(),
        }


def months() -> tuple:
    return (
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    )
