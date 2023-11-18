from datetime import timedelta

DAYS_PER_YEAR = 365.25


def years_int_to_time_delta(years):
    return timedelta(DAYS_PER_YEAR * years)


class PreservDuration:
    def __init__(self) -> None:
        pass


class ConcretePreservDuration(PreservDuration):
    def __init__(self, years) -> None:
        super().__init__()
        if isinstance(years, list):
            self.years = years
        else:
            self.years = [0, years]
        self.time_deltas = map(lambda year: yearsIntToTimeDelta(year), self.years)

    def __str__(self) -> str:
        return f"years: {self.years}"


class InfinitePreserveDuration(PreservDuration):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "infinite"
