from abc import ABC, abstractmethod
from incub_duration import DAYS_PER_YEAR

class IncubPeriod(ABC):
    @abstractmethod
    def periodInDays() : list[int]
    
class DayIncubPeriod(IncubPeriod):
    def __init__(self, days: list[int]) -> None:
        super().__init__()
        self.days = days
        
    def periodInDays(self):
        return self.days
    
    
class YearsIncubPeriod(IncubPeriod):
    def __init__(self, years: list[int]) -> None:
        super().__init__()
        self.days = map(years, lambda year: DAYS_PER_YEAR * year)
        
    def periodInDays(self):
        return self.days
    
class UnknownIncubPeriod(IncubPeriod):
    def __init__(self) -> None:
        super().__init__()
        
    def periodInDays(self):
        return []