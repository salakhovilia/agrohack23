from encoded_to_probabilities_mapper import PeriodValuesProvider, SlidingWindowIncubPeriodAccumulator, WeightsProvider
from illness_optimal import IllnessOptimal, WellDefinedIllnessOptimal
from illness_start import AbsIllnessStart, IllnessStart
from incub_period import IncubPeriod, HourIncubPeriod, UnknownIncubPeriod
from preserv_duration import PreservDuration, ConcretePreservDuration
from raw_data_to_cases_mapper import illn_optimal, illn_start, illn_none

periodValuesProvider = PeriodValuesProvider(use_hours=True)


class IllnessCaseMock():
    def __init__(self,
                 preservation_duration: PreservDuration,
                 illness_begin: AbsIllnessStart,
                 illness_optimal: IllnessOptimal,
                 incub_period: IncubPeriod,
                 ) -> None:
        super().__init__()

        self.preservation_duration = preservation_duration
        self.illness_begin = illness_begin
        self.illness_optimal = illness_optimal
        self.incub_period = incub_period


INCUB_PERIOD_5 = 5

illness_mock_5 = IllnessCaseMock(
    ConcretePreservDuration(years=1),
    IllnessStart(temp=15, hum=[0.8, 0.9]),
    WellDefinedIllnessOptimal(temps=[18, 20], hums=[0.8, 0.9]),
    HourIncubPeriod(hours=[INCUB_PERIOD_5, 10]),
)

INCUB_PERIOD_2 = 2
illness_mock_2 = IllnessCaseMock(
    ConcretePreservDuration(years=1),
    IllnessStart(temp=15, hum=[0.8, 0.9]),
    WellDefinedIllnessOptimal(temps=[18, 20], hums=[0.8, 0.9]),
    HourIncubPeriod(hours=[INCUB_PERIOD_2, 10]),
)

encoded_values_5 = [
    illn_optimal(),
    illn_start(),
    illn_start(),

    illn_start(),
    illn_none(),

    illn_optimal(),
    illn_optimal(),
    illn_optimal(),
    illn_none(),
    illn_none()
]

slidingWindowIncubAccumulator5 = SlidingWindowIncubPeriodAccumulator(
    illness=illness_mock_5,
    encoded_values=encoded_values_5,
    period_values_provider=periodValuesProvider,
    weights_provider=WeightsProvider()
)


def test_accumulator_uses_corrct_incub_period():
    assert INCUB_PERIOD_5 == slidingWindowIncubAccumulator5.get_incub_period()[0]


def test_accumulator_correctly_calculates_value_for_sliding_window_range():
    aggregated_value = slidingWindowIncubAccumulator5.get_value_for_range(index_start=0,
                                                                          index_end_non_incl=INCUB_PERIOD_5)

    assert aggregated_value == 0.32


def test_accumulator_correctly_calculates_value_for_sliding_window_range2():
    aggregated_value = slidingWindowIncubAccumulator5.get_value_for_range(index_start=3,
                                                                          index_end_non_incl=INCUB_PERIOD_5 + 3)

    assert aggregated_value == 0.64


def test_accumulator_correctly_aggregates():
    encoded_values_2 = [
        illn_optimal(),
        illn_start(),

        illn_start(),
        illn_start(),

        illn_none(),
        illn_optimal(),
    ]

    slidingWindowIncubAccumulator2 = SlidingWindowIncubPeriodAccumulator(
        illness=illness_mock_2,
        encoded_values=encoded_values_2,
        period_values_provider=periodValuesProvider,
        weights_provider=WeightsProvider()
    )
    mapped = slidingWindowIncubAccumulator2.map()

    assert mapped == [None, 0.6, 0.2, 0.2, 0.1, 0.5]


def test_doesnt_calc_for_non_incub_illness():
    enc_values = [illn_optimal(), illn_start()]
    slidingWindowIncubAccumulator2 = SlidingWindowIncubPeriodAccumulator(
        illness=IllnessCaseMock(
            ConcretePreservDuration(years=1),
            IllnessStart(temp=15, hum=[0.8, 0.9]),
            WellDefinedIllnessOptimal(temps=[18, 20], hums=[0.8, 0.9]),
            UnknownIncubPeriod(),
        ),
        encoded_values=enc_values,
        period_values_provider=periodValuesProvider,
        weights_provider=WeightsProvider()
    )
    mapped = slidingWindowIncubAccumulator2.map()

    assert mapped == enc_values
