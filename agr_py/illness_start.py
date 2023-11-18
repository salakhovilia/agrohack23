        
from abc import ABC, abstractmethod

from weather import Weather

def targetTempInTemps(targetTemp : float, temps: list[float]) -> bool:
    return temps[0] <= targetTemp and targetTemp <= temps[1]

def targetHumInHums(targetHum : float, hums: list[float]) -> bool:
    return hums[0] <= targetHum and targetHum <= hums[1]


class AbsIllnessStart(ABC):
    def __init__(self) -> None:
        super().__init__()
        
    @abstractmethod
    def matches(self, weather: Weather) -> bool:
        pass

class WTF_PH_IllnessStart(ABC):
    def __init__(self, ph : list[float]) -> None:
        super().__init__()
        self.ph = ph
    def __str__(self) -> str:
        return f"PH {self.ph}"
    def matches(self, weather : Weather):
        return False
    
class IllnessStart(AbsIllnessStart):
    def __init__(self, temp: float, hum) -> None:
        self.temp = temp 
        self.hum = hum
        if isinstance(temp, list):
            self.temp = temp
        else:
            self.temp = [temp,temp]
        if isinstance(hum , list):
            self.hum = hum
        else:
            self.hum = [hum, hum]
    def __str__(self) -> str:
        return f"temp {self.temp}, hum {self.hum}"
    
    def matches(self, weather : Weather): 
        return targetTempInTemps(weather.temp(), self.temp) and\
            targetHumInHums(weather.hum())
    

class UnknownIllnessStart(AbsIllnessStart):
    def __init__(self) -> None:
        super().__init__()
    def __str__(self) -> str:
        return "unknown"

    def matches(self, weather: Weather) -> bool:
        return False