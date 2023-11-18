from illness_cases_spec import IllnessCase
from raw_data_to_cases_mapper import IllnessDays, map_weather_to_historic_data, IllnessDayEnc


def test_raw_data_to_cases_mapper():
    illness_days: IllnessDays = map_weather_to_historic_data(
        dayly_temps=[15],
        dayly_hum=[0.5]
    )
    gray_gnill_days = illness_days.get_illness_historic_data(IllnessCase.GRAY_GNILL)

    assert IllnessDayEnc.NONE_CONDITION_SATISF in gray_gnill_days


def test_gray_gnill_mapping_start_satisfied_by_hum():
    illness_days: IllnessDays = map_weather_to_historic_data(
        dayly_temps=[15],
        dayly_hum=[0.96]
    )
    gray_gnill_days = illness_days.get_illness_historic_data(IllnessCase.GRAY_GNILL)
    assert IllnessDayEnc.START_CONDITION_SATISF in gray_gnill_days


def test_gray_gnill_mapping_optim_satisfied_by_hum():
    illness_days: IllnessDays = map_weather_to_historic_data(
        dayly_temps=[25],
        dayly_hum=[0.99]
    )
    gray_gnill_days = illness_days.get_illness_historic_data(IllnessCase.GRAY_GNILL)
    assert IllnessDayEnc.OPTIMAL_CONDITION_SATISF in gray_gnill_days

