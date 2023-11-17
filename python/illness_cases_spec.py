from ast import List
from enum import Enum
from abc import ABC, abstractmethod
from python.illness_optimal import IllnessOptimal, WellDefinedIllnessOptimal
from python.illness_start import IllnessStart
from python.incub_duration import ConcreteIncubDuration, IncubDuration
        
class IllnessCase(Enum):
    MILDEW = (
        ConcreteIncubDuration(years=5),
        IllnessStart(temp=11,hum=0.85),
        WellDefinedIllnessOptimal(temps=[21,25], hums=None)
    )
    
    def __init__(self,
                 preservation_duration: IncubDuration,
                 illness_begin: IllnessStart | None,
                 illness_optimal: IllnessOptimal | None,
                 ) -> None:
        super().__init__()
        
        self.preservation_duration = preservation_duration
        self.illness_begin = illness_begin
        self.illness_optimal = illness_optimal
