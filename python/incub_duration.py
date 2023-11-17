from datetime import timedelta


DAYS_PER_YEAR = 365.25

def yearsIntToTimeDelta(years):
    return timedelta(DAYS_PER_YEAR * years)

class PreservDuration:
    def __init__(self) -> None:
        pass

class ConcretePreservDuration(PreservDuration):
    def __init__(self, years) -> None:
        super().__init__()
        self.timedelta = yearsIntToTimeDelta(years)
        print("timedelta days:" + self.timedelta.days)

class InfinitePreserveDuration(PreservDuration):
    def __init__(self) -> None:
        super().__init__()        
        