from ast import List
from enum import Enum
from abc import ABC, abstractmethod
from python.illness_optimal import IllnessOptimal, WellDefinedIllnessOptimal
from python.illness_start import AbsIllnessStart, IllnessStart, UnknownIllnessStart
from python.incub_duration import ConcretePreservDuration, PreservDuration
from python.incub_period import DayIncubPeriod, IncubPeriod, UnknownIncubPeriod
        
class IllnessCase(Enum):
    MILDEW = (
        ConcretePreservDuration(years=5),
        IllnessStart(temp=11,hum=0.85),
        # todo : need to consider specific type of weather: капельная влага
        WellDefinedIllnessOptimal(temps=[21,25], hums=None),
        DayIncubPeriod(days=[11,15])
    ),
    OIDIUM = (
        ConcretePreservDuration(years=1),
        IllnessStart(temp=5, hum=[0.6,0.8]),
        # todo: need to consider conidiy vs mitseliy
        WellDefinedIllnessOptimal(temps=[25,35], hums=[0.6,0.8]),
        DayIncubPeriod(days=[7,14]),
    ),
    ANTRACNOS = (
        ConcretePreservDuration(years=1),
        IllnessStart(temp=[10,15], hum=[0.7,0.8]),
        # todo: need to consider conidiy vs mitseliy
        WellDefinedIllnessOptimal(temps=[24,30], hums=[0.7,0.8]),
        DayIncubPeriod(days=[3,4]),
    ),
    GRAY_GNILL = (
        ConcretePreservDuration(years=4),
        IllnessStart(temp=12, hum=[0.95,1]),
        # todo: need to consider conidiy vs mitseliy
        WellDefinedIllnessOptimal(temps=[25,30], hums=[0.99, 1.5]),
        DayIncubPeriod(days=[4,5]),
    ),
    BLACK_PYATNISTS = (
        ConcretePreservDuration(years=1),
        IllnessStart(temp=15, hum=[0.8,0.9]),
        # todo: need to consider conidiy vs mitseliy
        WellDefinedIllnessOptimal(temps=[18,20], hums=[0.8, 0.9]),
        DayIncubPeriod(days=[14,15]),
    ),
    BLACK_GNILL = (
        ConcretePreservDuration(years=1),
        UnknownIllnessStart(),
        # todo: need to consider conidiy vs mitseliy
        WellDefinedIllnessOptimal(temps=[20,25], hums=None),
        UnknownIncubPeriod(),
    ),
    
    
    def __init__(self,
                 preservation_duration: PreservDuration,
                 illness_begin: AbsIllnessStart | None,
                 illness_optimal: IllnessOptimal | None,
                 incub_period : IncubPeriod,
                 ) -> None:
        super().__init__()
        
        self.preservation_duration = preservation_duration
        self.illness_begin = illness_begin
        self.illness_optimal = illness_optimal
