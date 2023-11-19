from illness_cases_spec import IllnessCase
from weather import Weather, WeatherData
from enum import Enum


class IllnessConditEnc(Enum):
    NONE_CONDITION_SATISF = 0
    START_CONDITION_SATISF = 1
    OPTIMAL_CONDITION_SATISF = 2


def illn_none():
    return IllnessConditEnc.NONE_CONDITION_SATISF


def illn_start():
    return IllnessConditEnc.START_CONDITION_SATISF


def illn_optimal():
    return IllnessConditEnc.OPTIMAL_CONDITION_SATISF


illness_historic_data = list[IllnessConditEnc]


class IllnessEntry:
    def __init__(self, illness: IllnessCase) -> None:
        self.illness = illness
        self.illness_days_enc: illness_historic_data = []

    def add_start_condition_satisfied(self):
        self.illness_days_enc.append(IllnessConditEnc.START_CONDITION_SATISF)

    def add_optimal_condition_satisfied(self):
        self.illness_days_enc.append(IllnessConditEnc.OPTIMAL_CONDITION_SATISF)

    def add_none_condition_satisfied(self):
        self.illness_days_enc.append(IllnessConditEnc.NONE_CONDITION_SATISF)


class HistoryContext():
    def __init__(self) -> None:
        self.illness_entries: dict[IllnessCase, IllnessEntry] = {}
        pass

    def entry_for_illness(self, illness: IllnessCase) -> IllnessEntry:
        if illness not in self.illness_entries:
            illness_entry = IllnessEntry(illness=illness)
            self.illness_entries[illness] = illness_entry

        return self.illness_entries[illness]


class IllnessDays:
    def __init__(self) -> None:
        self.illness_to_historic_data: dict[IllnessCase, illness_historic_data] = {}
        pass

    def add_illness_entry(self, illness_entry: IllnessEntry):
        self.illness_to_historic_data[illness_entry.illness] = illness_entry.illness_days_enc

    def get_illness_historic_data(self, illness: IllnessCase) -> illness_historic_data:
        return self.illness_to_historic_data[illness]


def map_single_time_weather_to_illnesses_enc(
        weather: Weather,
        history: HistoryContext,
):
    for illness in IllnessCase:
        illness_entry = history.entry_for_illness(illness=illness)

        if illness.illness_at_optimal(weather=weather):
            illness_entry.add_optimal_condition_satisfied()
        elif illness.illness_can_start(weather=weather):
            illness_entry.add_start_condition_satisfied()
        else:
            illness_entry.add_none_condition_satisfied()


def map_weather_to_historic_data(
        temps: list[float],
        hums: list[float]
) -> IllnessDays:
    history_context = HistoryContext()

    for temp, hum in zip(temps, hums):
        weather = WeatherData(temp=temp, hum=hum)
        map_single_time_weather_to_illnesses_enc(
            weather=weather,
            history=history_context
        )

    acc_illness_days = IllnessDays()

    for illness in IllnessCase:
        acc_illness_days.add_illness_entry(history_context.entry_for_illness(illness=illness))

    return acc_illness_days
