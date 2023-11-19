from abc import ABC, abstractmethod
from preserv_duration import DAYS_PER_YEAR


class IncubPeriod(ABC):
    @abstractmethod
    def periodInDays(self) -> list[int]:
        pass

    @abstractmethod
    def periodInHours(self) -> list[int]:
        pass


class HourIncubPeriod(IncubPeriod):
    def __init__(self, hours: list[int]) -> None:
        super().__init__()
        self.hours = hours
        self.days = list(map(lambda hour: hour / 24, hours))

    def periodInDays(self):
        return self.days

    def periodInHours(self) -> list[int]:
        return self.hours

    def __str__(self) -> str:
        return f"period in days {self.days}"


class DayIncubPeriod(IncubPeriod):
    def __init__(self, days: list[int]) -> None:
        super().__init__()
        self.days = days
        self.hours = list(map(lambda day: day * 24, self.days))

    def periodInDays(self):
        return self.days

    def periodInHours(self) -> list[int]:
        return self.hours

    def __str__(self) -> str:
        return f"period in days {self.days}"


class YearsIncubPeriod(IncubPeriod):
    def __init__(self, years: list[int]) -> None:
        super().__init__()
        self.days = list(map(lambda year: DAYS_PER_YEAR * year, years))
        self.years = years
        self.hours = list(map(lambda day: day * 24, self.days))

    def periodInDays(self) -> list[int]:
        return self.days

    def periodInHours(self) -> list[int]:
        return self.hours

    def __str__(self) -> str:
        return f"period in years {self.years}"


class UnknownIncubPeriod(IncubPeriod):
    def periodInHours(self) -> list[int]:
        return []

    def __init__(self) -> None:
        super().__init__()

    def periodInDays(self):
        return []

    def __str__(self) -> str:
        return "unknown"
