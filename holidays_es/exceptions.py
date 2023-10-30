class ProvinceError(ValueError):
    """Exception if province is not valid."""


class YearError(ValueError):
    """Exception if year is not valid."""


class HolidaySpainError(Exception):
    """Exception if it is not possible to fetch the holidays."""
