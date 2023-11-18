        
from abc import ABC, abstractmethod

class AbsIllnessStart(ABC):
    pass

class WTF_PH_IllnessStart(ABC):
    def __init__(self, ph : list[float]) -> None:
        super().__init__()
        self.ph = ph

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

class UnknownIllnessStart(AbsIllnessStart):
    def __init__(self) -> None:
        super().__init__()
