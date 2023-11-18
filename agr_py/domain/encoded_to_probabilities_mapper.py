from incub_period import UnknownIncubPeriod, IncubPeriod
from illness_cases_spec import IllnessCase
from raw_data_to_cases_mapper import IllnessDays, IllnessDayEnc


def normalize_weighted_average(value: float) -> float:
    min_value = get_weight(IllnessDayEnc.NONE_CONDITION_SATISF)
    return (value - min_value) / (get_weight(IllnessDayEnc.OPTIMAL_CONDITION_SATISF) - min_value)


def get_weight(illness_case: IllnessDayEnc):
    if IllnessDayEnc.NONE_CONDITION_SATISF == illness_case:
        return 0.5
    elif IllnessDayEnc.START_CONDITION_SATISF == illness_case:
        return 1
    elif IllnessDayEnc.OPTIMAL_CONDITION_SATISF == illness_case:
        return 3


class IllnessProbabilities():
    def __init__(self):
        self.illness_to_prob: dict[IllnessCase, float] = {}


class TimeSeriesCharacteristicsAccumulator():

    # the conditional probability of each streak
    # duration weighted score
    # the frequency of each streak
    # the average streak length
    # the standard deviation of streak lengths
    def __init__(self):
        pass




class PeriodValuesProvider():
    def __init__(self, use_hours: bool = True):
        self.use_hours = use_hours
        pass

    def get_incub_period_in_time_unit(self, incub_period: IncubPeriod):
        if self.use_hours:
            return incub_period.periodInHours()
        else:
            return incub_period.periodInDays()


class SlidingWindowIncubPeriodAccumulator():
    def __init__(self, illness: IllnessCase, encoded_values: list[IllnessDayEnc],
                 period_values_provider: PeriodValuesProvider):
        self.illness = illness
        self.period_values_provider = period_values_provider
        self.prev_stage_values = encoded_values

    def get_value_for_range(self, index_start: int, index_end_non_incl: int) -> float:
        prev_stage_value = self.prev_stage_values

        acc = 0

        for i in range(index_start, index_end_non_incl):
            value = prev_stage_value[i]
            acc += get_weight(illness_case=value)

        range_value = index_end_non_incl - index_start

        raw_average = acc / float(range_value)

        return normalize_weighted_average(raw_average)

    def get_incub_period(self):
        return self.period_values_provider.get_incub_period_in_time_unit(self.illness.incub_period)

    def map(self) -> list[float] | list[IllnessDayEnc]:
        if isinstance(self.illness.incub_period, UnknownIncubPeriod):
            return self.prev_stage_values

        size = len(self.prev_stage_values)
        target_arr = []

        incub_period = self.get_incub_period()

        earliest_incub_period = incub_period[0]

        for i in range(0, earliest_incub_period - 1):
            target_arr.append(None)

        for i in range(earliest_incub_period - 1, size):
            sliding_window_value = self.get_value_for_range(
                index_start=i - (earliest_incub_period - 1),
                index_end_non_incl=i+1
            )
            target_arr.append(sliding_window_value)

        return target_arr


def map_encoded_to_probabilities(illness_days: IllnessDays) -> IllnessProbabilities:
    for illness in IllnessCase:
        illness_day_series = illness_days.get_illness_historic_data(illness)
        # map in a sliding window manner the illnesses with
