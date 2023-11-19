import json

from encoded_to_probabilities_mapper import WeightsProvider, PeriodValuesProvider, SlidingWindowIncubPeriodAccumulator, \
    ForTargetDateWeightedExponentialAccumulator
from illness_cases_spec import IllnessCase
from raw_data_to_cases_mapper import IllnessConditEnc, map_weather_to_historic_data


def get_illness_encoded(temps: list[float],
                        hums: list[float]
                        ):
    encoded_data = map_weather_to_historic_data(temps, hums)

    # todo need to better serialize this
    return json.dumps(encoded_data)


def get_illness_prob_for_each_timeunit_def(
        temps: list[float],
        hums: list[float],
        illness_name: str,
) -> list[float] | None:
    return get_illness_prob_for_each_timeunit(
        none_satisf_weight=0.5,
        partially_satisf_weight=1.0,
        optimally_satisf_weight=3.0,
        exp_growth_weight=0.1,
        temps=temps,
        hums=hums,
        illness_name=illness_name
    )


def map_hums(source_hums: list[float]) -> list[float]:
    return list(map(lambda hum: hum / 100.0, source_hums))


def get_illness_prob_for_each_timeunit(none_satisf_weight: float,
                                       partially_satisf_weight: float,
                                       optimally_satisf_weight: float,
                                       exp_growth_weight: float,
                                       temps: list[float],
                                       hums: list[float],
                                       illness_name: str,
                                       ) -> list[float] | None:
    weight_provider = WeightsProvider(
        weight_map={
            IllnessConditEnc.NONE_CONDITION_SATISF: none_satisf_weight,
            IllnessConditEnc.START_CONDITION_SATISF: partially_satisf_weight,
            IllnessConditEnc.OPTIMAL_CONDITION_SATISF: optimally_satisf_weight
        },
        lambda_factor=exp_growth_weight
    )

    period_values_provider = PeriodValuesProvider()

    illness = None
    for i in IllnessCase:
        if i.name == illness_name:
            illness = i

    if illness is None:
        return None

    # encoding historic data
    mapped_data = map_weather_to_historic_data(temps, hums)

    per_illness_mapped_data = mapped_data.get_illness_historic_data(illness)

    # considering incubation period whether possible

    sliding_window_incub_period_acc = SlidingWindowIncubPeriodAccumulator(
        illness=illness,
        encoded_values=per_illness_mapped_data,
        period_values_provider=period_values_provider,
        weights_provider=weight_provider
    )

    if sliding_window_incub_period_acc.is_applicable():
        sliding_window_acc_probs_normalized = sliding_window_incub_period_acc.map()
        return sliding_window_acc_probs_normalized
    else:
        expon_weight_acc = ForTargetDateWeightedExponentialAccumulator(
            illness=illness,
            encoded_values=per_illness_mapped_data,
            illness_day_enc_weight_provider=weight_provider
        )

        expon_weights_mapped = expon_weight_acc.map()
        return expon_weights_mapped
