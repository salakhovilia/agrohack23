from abc import ABC, abstractmethod

from weather import Weather

class IllnessOptimal(ABC):
    @abstractmethod
    def check_weather_satisfies_this_condition(weather: Weather) -> bool:
        pass
        
# пока решил остановиться на простом дефинишене оптимальных условий,
# всякую пболее подробную залупу потом докрутим как чеды
class WellDefinedIllnessOptimal(IllnessOptimal):
    def __init__(self, temps: list[float], hums: list[float] | None) -> None:
        super().__init__()
        self.temps = temps
        self.hums = hums
        
    def check_weather_satisfies_this_condition(weather: Weather) -> bool:
        # todo заимплементить нормально
        return False
    
    def __str__(self) -> str:
        return f"temperatures {self.temps}, humidity {self.hums}"