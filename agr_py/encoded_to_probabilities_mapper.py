from illness_cases_spec import IllnessCase
from raw_data_to_cases_mapper import IllnessDays


class IllnessProbabilities():
    def __init__(self):
        self.illness_to_prob : dict[IllnessCase, float] = {}

class TimeSeriesCharacteristicsAccumulator():
    # the conditional probability of each streak
    # duration weighted score
    # the frequency of each streak
    # the average streak length
    # the standard deviation of streak lengths
    def __init__(self):
        pass


def map_encoded_to_probabilities(illness_days : IllnessDays) -> IllnessProbabilities:
    for illness in IllnessCase:
        illness_day_series = illness_days.get_illness_historic_data(illness)
        # accumulate data per one illness

