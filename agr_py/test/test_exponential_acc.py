from encoded_to_probabilities_mapper import ForTargetDateWeightedExponentialAccumulator, WeightsProvider
from illness_optimal import WellDefinedIllnessOptimal
from illness_start import IllnessStart
from incub_period import HourIncubPeriod
from preserv_duration import ConcretePreservDuration
from raw_data_to_cases_mapper import illn_optimal, illn_start, illn_none
from test_sliding_window_incub import IllnessCaseMock

encoded_values_2 = [
    illn_optimal(),
    illn_start(),

    illn_start(),
    illn_start(),

    illn_none(),
    illn_optimal(),
]
INCUB_PERIOD_2 = 2

illness_mock_2 = IllnessCaseMock(
    ConcretePreservDuration(years=1),
    IllnessStart(temp=15, hum=[0.8, 0.9]),
    WellDefinedIllnessOptimal(temps=[18, 20], hums=[0.8, 0.9]),
    HourIncubPeriod(hours=[INCUB_PERIOD_2, 10]),
)

for_target_date_weighted_exp_acc = ForTargetDateWeightedExponentialAccumulator(
    illness=illness_mock_2,
    encoded_values=encoded_values_2,
    illness_day_enc_weight_provider=WeightsProvider(lambda_factor=0.1),
)

def test_exp_growth_probs():
    mapped = for_target_date_weighted_exp_acc.map()
    assert mapped == []