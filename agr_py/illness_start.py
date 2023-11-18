        
from abc import ABC, abstractmethod

class AbsIllnessStart(ABC):
    pass

class WTF_PH_IllnessStart(ABC):
    def __init__(self, ph : list[float]) -> None:
        super().__init__()
        self.ph = ph
    def __str__(self) -> str:
        return f"PH {self.ph}"

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

class UnknownIllnessStart(AbsIllnessStart):
    def __init__(self) -> None:
        super().__init__()
    def __str__(self) -> str:
        return "unknown"
