import math

from incub_period import UnknownIncubPeriod, IncubPeriod
from illness_cases_spec import IllnessCase
from raw_data_to_cases_mapper import IllnessDays, IllnessDayEnc


class WeightsProvider:
    def __init__(self, weight_map=None, lambda_factor=None):
        if weight_map is None:
            weight_map = {IllnessDayEnc.NONE_CONDITION_SATISF: 0.5,
                          IllnessDayEnc.START_CONDITION_SATISF: 1,
                          IllnessDayEnc.OPTIMAL_CONDITION_SATISF: 3}
        if lambda_factor is None:
            lambda_factor = 0.1
        self.weight_map = weight_map
        self.lambda_factor = lambda_factor

    def get_weight(self, illness_case: IllnessDayEnc):
        return self.weight_map[illness_case]

    def get_exponential_growth_factor(self) -> float:
        return self.weight_map


def normalize_weighted_average(value: float, illnessDayEncWeightProvider: WeightsProvider) -> float:
    min_value = illnessDayEncWeightProvider.get_weight(IllnessDayEnc.NONE_CONDITION_SATISF)
    return (value - min_value) / (
            illnessDayEncWeightProvider.get_weight(IllnessDayEnc.OPTIMAL_CONDITION_SATISF) - min_value)


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


class SlidingWindowIncubPeriodAccumulator:
    def __init__(self, illness: IllnessCase, encoded_values: list[IllnessDayEnc],
                 period_values_provider: PeriodValuesProvider,
                 weights_provider: WeightsProvider
                 ):
        self.illness = illness
        self.period_values_provider = period_values_provider
        self.prev_stage_values = encoded_values
        self.illness_day_enc_weight_provider = weights_provider

    def get_value_for_range(self, index_start: int, index_end_non_incl: int) -> float:
        prev_stage_value = self.prev_stage_values

        acc = 0

        for i in range(index_start, index_end_non_incl):
            value = prev_stage_value[i]
            acc += self.illness_day_enc_weight_provider.get_weight(illness_case=value)

        range_value = index_end_non_incl - index_start

        raw_average = acc / float(range_value)

        return normalize_weighted_average(raw_average, self.illness_day_enc_weight_provider)

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
                index_end_non_incl=i + 1
            )
            target_arr.append(sliding_window_value)

        return target_arr


def map_encoded_to_probabilities(illness_days: IllnessDays) -> IllnessProbabilities:
    for illness in IllnessCase:
        illness_day_series = illness_days.get_illness_historic_data(illness)
        # map in a sliding window manner the illnesses with


class ForTargetDateWeightedExponentialAccumulator():
    def __init__(self,
                 illness: IllnessCase,
                 encoded_values: list[IllnessDayEnc],
                 illness_day_enc_weight_provider: WeightsProvider):
        self.illness = illness
        self.encoded_values = encoded_values
        self.weights_provider = illness_day_enc_weight_provider

    def get_weighted_value(self, value: IllnessDayEnc, index: int) -> float:
        total_length = len(self.encoded_values)

        base_weight = self.weights_provider.get_weight(illness_case=value)
        distance_from_end = total_length - (index + 1)
        adjusted_weight = self.adjust_exponential_weight(distance_from_end, total_length)
        return base_weight * adjusted_weight

    def adjust_exponential_weight(self, distance_from_end: int, total_length: int) -> float:
        # Exponential growth function
        lambda_factor = self.weights_provider.lambda_factor  # Adjust this to control the rate of growth
        # The factor should decrease as the distance from the end decreases
        normalized_distance = distance_from_end / total_length
        return math.exp(lambda_factor * (normalized_distance - 1))

    # def normalize_weights(self, weights: list[float]) -> list[float]:
    #     max_value = max(weights)
    #     normalized_values = [val / max_value for val in weights]
    #     return normalized_values

    def normalize_weights(self, weights: list[float]) -> list[float]:
        total_weight_sum = sum(weights)
        return [weight / total_weight_sum for weight in weights]

    def map(self) -> list[float]:
        size = len(self.encoded_values)
        target_arr = []

        for i, value in enumerate(self.encoded_values):
            weighted_value = self.get_weighted_value(value, i)
            target_arr.append(weighted_value)

        # Normalize the values to convert into probabilities
        return self.normalize_weights(target_arr)
