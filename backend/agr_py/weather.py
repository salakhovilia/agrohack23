from abc import ABC, abstractmethod

class Weather(ABC): 
    @abstractmethod
    def temp(self) -> float:
        pass
    @abstractmethod
    def hum(self) -> float | None:
        pass
    
    @abstractmethod
    def humtype(self):
        # некоторые из пунктов таблички кекнутые, закрыл этой абстракцией пока
        pass

class WeatherData(Weather):
    def __init__(self, temp, hum) -> None:
        super().__init__()
        self.temp_value = temp
        self.hum_value = hum
    
    def temp(self):
        return self.temp_value
    
    def hum(self):
        return self.hum_value
    
    def humtype(self):
        raise Exception("не вызывайте этот метод, пожалуйста")