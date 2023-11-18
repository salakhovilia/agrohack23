from abc import ABC, abstractmethod

from weather import Weather


def target_temp_in_temps(target_temp: float, temps: list[float]) -> bool:
    return temps[0] <= target_temp <= temps[1]


def target_hum_in_hums(target_hum: float, hums: list[float]) -> bool:
    return hums[0] <= target_hum <= hums[1]


class AbsIllnessStart(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def matches(self, weather: Weather) -> bool:
        pass


class WTF_PH_IllnessStart(ABC):
    def __init__(self, ph: list[float]) -> None:
        super().__init__()
        self.ph = ph

    def __str__(self) -> str:
        return f"PH {self.ph}"

    def matches(self, weather: Weather):
        return False


class IllnessStart(AbsIllnessStart):
    def __init__(self, temp: float, hum) -> None:
        super().__init__()
        self.temp = temp
        self.hum = hum
        if isinstance(temp, list):
            self.temp = temp
        else:
            self.temp = [temp, temp]
        if isinstance(hum, list):
            self.hum = hum
        else:
            self.hum = [hum, hum]

    def __str__(self) -> str:
        return f"temp {self.temp}, hum {self.hum}"

    def matches(self, weather: Weather):
        return (target_temp_in_temps(weather.temp(), self.temp) or \
                self.temp[1] <= weather.temp()) and \
            target_hum_in_hums(weather.hum(), self.hum)


class UnknownIllnessStart(AbsIllnessStart):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "unknown"

    def matches(self, weather: Weather) -> bool:
        return False
