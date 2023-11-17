from datetime import timedelta


days_per_year = 365.25

def yearsIntToTimeDelta(years):
    return timedelta(days_per_year * years)

class IncubDuration:
    def __init__(self) -> None:
        pass

class ConcreteIncubDuration(IncubDuration):
    def __init__(self, years) -> None:
        super().__init__()
        self.timedelta = yearsIntToTimeDelta(years)
        print("timedelta days:" + self.timedelta.days)

class InfiniteIncubDuration(IncubDuration):
    def __init__(self) -> None:
        super().__init__()        
        