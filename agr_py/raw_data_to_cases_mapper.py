

from illness_cases_spec import IllnessCase
from weather import Weather, WeatherData

from enum import Enum

class IllnessDayEnc(Enum):
    NONE_CONDITION_SATISF = 0
    START_CONDITION_SATISF = 1
    OPTIMAL_CONDITION_SATISF = 2
    
illness_historic_data = list[IllnessDayEnc]

class IllnessEntry():
    def __init__(self, illness : IllnessCase) -> None:
        self.illness = illness
        self.illness_days_enc : illness_historic_data = []
    
    def add_start_condition_satisfied(self):
        self.illness_days_enc.append(IllnessDayEnc.START_CONDITION_SATISF)
        
    def add_optimal_condition_satisfied(self):
        self.illness_days_enc.append(IllnessDayEnc.OPTIMAL_CONDITION_SATISF)
        
    def add_none_condition_satisfied(self):
        self.illness_days_enc.append(IllnessDayEnc.NONE_CONDITION_SATISF)
    
class HistoryContext():
    def __init__(self) -> None:
        self.illness_entries : dict[IllnessCase, IllnessEntry] = {}
        pass
    
    def entry_for_illness(self, illness : IllnessCase) -> IllnessEntry:
        if illness not in self.illness_entries:
            illness_entry = IllnessEntry(illness=illness)
            self.illness_entries[illness] = illness_entry
            
        return self.illness_entries[illness]
    
class IllnessDays():
    def __init__(self) -> None:
        self.illness_to_historic_data : dict[IllnessCase, illness_historic_data] = {}
        pass
        
    def add_illness_entry(self, illness_entry : IllnessEntry):
        self.illness_to_historic_data[illness_entry.illness] = illness_entry.illness_days_enc

def map_single_time_weather_to_illnesses_days(
    weather: Weather,
    history : HistoryContext,
):
    for illness in IllnessCase:
        illness_entry = history.entry_for_illness(illness=illness)
        
        if illness.illness_at_optimal(weather=weather):
            illness_entry.add_optimal_condition_satisfied()
        elif illness.illness_can_start(weather=weather):
            illness_entry.add_start_condition_satisfied()
        else:
            illness_entry.add_none_condition_satisfied()
        
        print(f"iterating over {illness}", illness)
        
def map_weather_to_historic_data(
    dayly_temps : list[float],
    dayly_hum : list[float]
) -> IllnessDays:
    historyContext = HistoryContext()
    
    for temp, hum in zip(dayly_temps, dayly_hum):
        weather = WeatherData(temp=temp, hum=hum)
        map_single_time_weather_to_illnesses_days(
            weather=weather,
            history=historyContext
        )
        
        