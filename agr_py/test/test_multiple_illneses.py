from illness_cases_spec import IllnessCase
from raw_data_to_cases_mapper import map_weather_to_historic_data, IllnessDayEnc

common_temps = [14, 17, 15, 19, 25]
common_hums = [0.56, 0.80, 0.89, 0.45, 0.8]


def test_alternarioz_5_days():
    temps = common_temps
    hums = common_hums

    illness_days = map_weather_to_historic_data(temps, hums)

    illness = IllnessCase.ALTERNARIOZ

    assert [
               IllnessDayEnc.NONE_CONDITION_SATISF,
               IllnessDayEnc.START_CONDITION_SATISF,
               IllnessDayEnc.START_CONDITION_SATISF,
               IllnessDayEnc.NONE_CONDITION_SATISF,
               IllnessDayEnc.OPTIMAL_CONDITION_SATISF,
           ] == illness_days.get_illness_historic_data(illness)


def test_oidium_5_days():
    temps = common_temps
    hums = common_hums

    illness_days = map_weather_to_historic_data(temps, hums)

    illness = IllnessCase.OIDIUM

    assert [
               IllnessDayEnc.NONE_CONDITION_SATISF,
               IllnessDayEnc.START_CONDITION_SATISF,
               IllnessDayEnc.NONE_CONDITION_SATISF,
               IllnessDayEnc.NONE_CONDITION_SATISF,
               IllnessDayEnc.OPTIMAL_CONDITION_SATISF,
           ] == illness_days.get_illness_historic_data(illness)
