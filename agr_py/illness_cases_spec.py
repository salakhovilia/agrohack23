from ast import List
from enum import Enum
from abc import ABC, abstractmethod
from weather import Weather
from illness_optimal import IllnessOptimal, WellDefinedIllnessOptimal
from illness_start import AbsIllnessStart, IllnessStart, UnknownIllnessStart, WTF_PH_IllnessStart
from preserv_duration import ConcretePreservDuration, InfinitePreserveDuration, PreservDuration
from incub_period import DayIncubPeriod, IncubPeriod, UnknownIncubPeriod, YearsIncubPeriod
        
class IllnessCase(Enum):
    MILDEW = (
        ConcretePreservDuration(years=5),
        IllnessStart(temp=11,hum=[0.85, 1.5 ]),
        # todo : need to consider specific type of weather: капельная влага
        WellDefinedIllnessOptimal(temps=[21,25], hums=None),
        DayIncubPeriod(days=[11,15])
    )
    OIDIUM = (
        ConcretePreservDuration(years=1),
        IllnessStart(temp=5, hum=[0.6,0.8]),
        # todo: need to consider conidiy vs mitseliy
        WellDefinedIllnessOptimal(temps=[25,35], hums=[0.6,0.8]),
        DayIncubPeriod(days=[7,14]),
    )
    ANTRACNOS = (
        ConcretePreservDuration(years=5),
        IllnessStart(temp=[10,15], hum=[0.7,0.8]),
        WellDefinedIllnessOptimal(temps=[24,30], hums=[0.7,0.8]),
        DayIncubPeriod(days=[3,4]),
    )
    GRAY_GNILL = (
        ConcretePreservDuration(years=4),
        IllnessStart(temp=12, hum=[0.95,1]),
        WellDefinedIllnessOptimal(temps=[25,30], hums=[0.99, 1.5]),
        DayIncubPeriod(days=[4,5]),
    )
    BLACK_PYATNISTS = (
        ConcretePreservDuration(years=1),
        IllnessStart(temp=15, hum=[0.8,0.9]),
        WellDefinedIllnessOptimal(temps=[18,20], hums=[0.8, 0.9]),
        DayIncubPeriod(days=[14,15]),
    )
    BLACK_GNILL = (
        ConcretePreservDuration(years=1),
        UnknownIllnessStart(),
        WellDefinedIllnessOptimal(temps=[20,25], hums=None),
        UnknownIncubPeriod(),
    )
    WHITE_GNILL = (
        ConcretePreservDuration(years=[3,4]),
        IllnessStart(temp=14,hum=[0.9, 1.5]),
        # todo: need to consider ливневые осадки
        WellDefinedIllnessOptimal(temps=[20,27], hums=[0.9, 1.5]),
        UnknownIncubPeriod(),
    )
    VILT = (
        ConcretePreservDuration(years=[3,4]),
        UnknownIllnessStart(),
        # todo: need to consider ППВ
        WellDefinedIllnessOptimal(temps=[21,24], hums=[0.5, 0.6]),
        YearsIncubPeriod(years=[1,2]),
    )
    ALTERNARIOZ = (
        ConcretePreservDuration(years=1),
        IllnessStart(temp=[11,15], hum=[0.8,0.9]),
        WellDefinedIllnessOptimal(temps=[23,25], hums=[0.8, 0.9]),
        UnknownIncubPeriod(),
    )
    FUZARIOZ = (
        InfinitePreserveDuration(),
        IllnessStart(temp=[1, 1000],hum=[0.4, 0.8]),
        WellDefinedIllnessOptimal(temps=[13,20], hums=[0.8, 0.9]),
        UnknownIncubPeriod(),
    )
    KRASNUHA = (
        ConcretePreservDuration(years=1),
        IllnessStart(temp=11,hum=[0.8, 0.9]),
        WellDefinedIllnessOptimal(temps=[18, 20], hums=[0.9,1.1]),
        UnknownIncubPeriod(),
    )
    BACT_CANCER = (
        ConcretePreservDuration(years=2),
        WTF_PH_IllnessStart(ph=[6.0, 9.0]),
        WellDefinedIllnessOptimal(temps=[25, 30], hums=[0.95,0.95]),
        UnknownIncubPeriod(),
    )
    
    def __init__(self,
                 preservation_duration: PreservDuration,
                 illness_begin: AbsIllnessStart,
                 illness_optimal: IllnessOptimal,
                 incub_period : IncubPeriod,
                 ) -> None:
        super().__init__()
        self.preservation_duration = preservation_duration
        self.illness_begin = illness_begin
        self.illness_optimal = illness_optimal
        self.incub_period = incub_period
    
    def __str__(self) -> str:
        return f"""
name          : {self.name}
preserv. dur. : {self.preservation_duration};
illness start : {self.illness_begin};
illness optim.: {self.illness_optimal};
incub period  : {self.incub_period};
"""

    def illness_can_start(self, weather: Weather) -> bool:
        return self.illness_begin.matches(weather)
    
    def  illness_at_optimal(self, weather: Weather) -> bool:
        return self.illness_optimal.check_weather_satisfies_this_condition(weather=weather)
    
    # def incub_period_satisfied(self, weather: Weather, history) -> bool