

from agr_py.illness_cases_spec import IllnessCase
from agr_py.weather import Weather

class HistoryContext():
    def __init__(self) -> None:
        
        pass
    
class Illnesses():
    def __init__(self, illnesses) -> None:
        self.illnesses = illnesses
        pass

def map_weather_and_history_to_illness(
    weather: Weather,
    history : HistoryContext,
) -> Illnesses:
    for illness in IllnessCase:
        print(f"iterating over {illness}", illness)