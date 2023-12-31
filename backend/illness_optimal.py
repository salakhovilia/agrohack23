from abc import ABC, abstractmethod

from weather import Weather
from illness_start import target_hum_in_hums, target_temp_in_temps


class IllnessOptimal(ABC):
    @abstractmethod
    def check_weather_satisfies_this_condition(self, weather: Weather) -> bool:
        pass


# пока решил остановиться на простом дефинишене оптимальных условий,
# всякую пболее подробную залупу потом докрутим как чеды
class WellDefinedIllnessOptimal(IllnessOptimal):
    def __init__(self, temps: list[float], hums: list[float] | None) -> None:
        super().__init__()
        self.temps = temps
        self.hums = hums

    def check_weather_satisfies_this_condition(self, weather: Weather) -> bool:
        # todo заимплементить нормально
        return target_temp_in_temps(weather.temp(), self.temps) and \
            (self.hums is None or target_hum_in_hums(weather.hum(), self.hums))

    def __str__(self) -> str:
        return f"temperatures {self.temps}, humidity {self.hums}"
