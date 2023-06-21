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
        self.__check_errors()

    def __check_errors(self):
        if self._soup.find(text="Warning") is not None:
            raise Exception("There are no records for the specified year.")
        if self._soup.find(text="Error:") is not None:
            raise Exception(
                f"The name is not in the list, try one of these: {', '.join(get_provinces())}."
            )

    def __tour_months(self, holiday):
        result = []
        for m in months():
            div_id = f"wrap{m.capitalize()}"
            div = self._soup.find(id=div_id)
            # find the div with class "wrapFestivos"
            div_wrap_festivos = div.find('div', { 'class' : 'wrapFestivos'})
            table_id = f"mes{m.title()}"
            table = self._soup.find(id=table_id)
            holidays = table.findAll("td", {"class": f"cajaFestivo{holiday}"})
            description = ''
            for h in holidays:
                description = get_description(div_wrap_festivos, holidays.index(h), holiday)
                day = int(h.get_text())
                month = months().index(m) + 1
                date = datetime.date(day=day, month=month, year=self.year)

                result.append({ 'date': date, 'description': description})

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
        
def get_description(div_wrap_festivos, index, holiday):
    if div_wrap_festivos:
        # Find all li elements inside div
        lis = div_wrap_festivos.find_all('li')
        lis_holidays = []
        for li in lis:
            # Chose those with a span element with class "festivoX"
            span_found = li.find_all('span', { 'class' : f'festivo{holiday}' })
            if span_found and len(span_found) == 1:
                lis_holidays.append(li.get_text().replace(span_found[0].string,''))
                
        return lis_holidays[index]

    return ''

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
