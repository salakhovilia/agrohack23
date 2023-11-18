from abc import ABC, abstractmethod
from preserv_duration import DAYS_PER_YEAR


class IncubPeriod(ABC):
    @abstractmethod
    def periodInDays(self) -> list[int]:
        pass


class DayIncubPeriod(IncubPeriod):
    def __init__(self, days: list[int]) -> None:
        super().__init__()
        self.days = days

    def periodInDays(self):
        return self.days

    def __str__(self) -> str:
        return f"period in days {self.days}"


class YearsIncubPeriod(IncubPeriod):
    def __init__(self, years: list[int]) -> None:
        super().__init__()
        self.days = map(lambda year: DAYS_PER_YEAR * year, years)
        self.years = years

    def periodInDays(self):
        return self.days

    def __str__(self) -> str:
        return f"period in years {self.years}"


class UnknownIncubPeriod(IncubPeriod):
    def __init__(self) -> None:
        super().__init__()

    def periodInDays(self):
        return []

    def __str__(self) -> str:
        return "unknown"
