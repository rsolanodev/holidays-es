import datetime
import logging

import requests
from bs4 import BeautifulSoup, Tag

from holidays_es import enums, exceptions, models


logger = logging.getLogger(__name__)


class HolidaySpain:
    """
    Retrieve holidays in Spain based on a province and year.
    """

    base_url: str = "https://www.calendarioslaborales.com"
    months: tuple[str, ...] = (
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    )
    scope_mappings: dict[str, enums.Scope] = {
        "festivoN": enums.Scope.NATIONAL,
        "festivoR": enums.Scope.REGIONAL,
        "festivoP": enums.Scope.LOCAL,
    }

    def __init__(
        self,
        province: enums.Province,
        year: int | None = None,
        min_year: int = 2006,
        max_year: int | None = None,
    ) -> None:
        self.min_year: int = min_year
        self.max_year: int = max_year or datetime.datetime.now().year

        self.province: str = self._validate_province(province)
        self.year: int = self._validate_year(year)
        self.holidays: tuple[models.Holiday, ...] = self._fetch_holidays()

    def _validate_year(self, year: int | None = None) -> int:
        year = year or datetime.datetime.now().year
        if year < self.min_year or year > self.max_year:
            raise exceptions.YearError(
                f"It is not possible to obtain the holidays for the year {year}."
            )
        return year

    def _validate_province(self, province: enums.Province) -> str:
        if not isinstance(province, enums.Province):
            raise exceptions.ProvinceError(
                f"'{province}' is not a valid province for Spain."
            )
        return province.value

    def _fetch_holidays(self) -> tuple[models.Holiday, ...]:
        """
        Fetch holidays for the province and year.
        """
        url = f"/calendario-laboral-{self.province}-{self.year}.htm"
        content = self._get_content(url=url)
        soup = BeautifulSoup(content, "html.parser")
        return self._parse_holidays(soup)

    def _get_content(self, url: str) -> bytes | None:
        """
        Fetch content of the given URL.
        """
        try:
            response = requests.get(f"{self.base_url}{url}", timeout=10)
            response.raise_for_status()
            return response.content
        except (requests.Timeout, requests.RequestException, requests.HTTPError):
            raise exceptions.HolidaySpainError(
                "Something is not working as it should! If the issue persists,"
                "consider updating to the latest version of the package."
            )

    def _parse_holidays(self, soup: BeautifulSoup) -> tuple[models.Holiday, ...]:
        """
        Parse holidays from the BeautifulSoup object.
        """
        holidays = []
        for month_tag in soup.find_all("div", class_="mes"):
            month_idx = self._get_month_index(month_tag.h3.text)
            for holiday_tag in month_tag.find_all("li"):
                holiday = self._parse_holiday_tag(holiday_tag, month_idx)
                holidays.append(holiday)
        return tuple(holidays)

    def _get_month_index(self, month_name: str):
        """
        Get month index based on its name.
        """
        return self.months.index(month_name) + 1

    def _parse_holiday_tag(self, holiday_tag: Tag, month_idx: int) -> models.Holiday:
        """
        Parse a holiday tag to extract the holiday information.
        """
        date_tag = holiday_tag.find("span")
        holiday_key = date_tag["class"][0]
        day_number = int(date_tag.text.split(" ")[0])

        holiday_tag.span.extract()
        description = holiday_tag.text.strip()

        date = datetime.date(day=day_number, month=month_idx, year=self.year)
        scope: enums.Scope = self.scope_mappings[holiday_key]
        return models.Holiday(scope=scope, date=date, description=description)  # type: ignore

    def _filter_by_scope(self, scope: enums.Scope) -> tuple[models.Holiday, ...]:
        """
        Filter holidays based on their scope.
        """
        return tuple(filter(lambda holiday: holiday.scope == scope, self.holidays))

    @property
    def national(self) -> tuple[models.Holiday, ...]:
        """
        Tuple of national holidays.
        """
        return self._filter_by_scope(enums.Scope.NATIONAL)

    @property
    def regional(self) -> tuple[models.Holiday, ...]:
        """
        Tuple of regional holidays.
        """
        return self._filter_by_scope(enums.Scope.REGIONAL)

    @property
    def local(self) -> tuple[models.Holiday, ...]:
        """
        Tuple of local holidays.
        """
        return self._filter_by_scope(enums.Scope.LOCAL)

    def find(self, date: datetime.date) -> models.Holiday | None:
        """
        Find the holiday from the date.
        """
        for holiday in self.holidays:
            if date == holiday.date:
                return holiday
        return None
