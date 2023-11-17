from abc import ABC, abstractmethod

class Weather(ABC): 
    @abstractmethod
    def temp() -> float:
        pass
    @abstractmethod
    def hum() -> float | None:
        pass
    
    @abstractmethod
    def humtype():
        # некоторые из пунктов таблички кекнутые, закрыл этой абстракцией пока
        pass

