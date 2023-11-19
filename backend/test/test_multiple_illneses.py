from illness_cases_spec import IllnessCase
from raw_data_to_cases_mapper import map_weather_to_historic_data, IllnessConditEnc

common_temps = [14, 17, 15, 19, 25]
common_hums = [0.56, 0.80, 0.89, 0.45, 0.8]


def test_alternarioz_5_days():
    temps = common_temps
    hums = common_hums

    illness_days = map_weather_to_historic_data(temps, hums)
    illness = IllnessCase.ALTERNARIOZ

    assert [
               IllnessConditEnc.NONE_CONDITION_SATISF,
               IllnessConditEnc.START_CONDITION_SATISF,
               IllnessConditEnc.START_CONDITION_SATISF,
               IllnessConditEnc.NONE_CONDITION_SATISF,
               IllnessConditEnc.OPTIMAL_CONDITION_SATISF,
           ] == illness_days.get_illness_historic_data(illness)


def test_oidium_5_days():
    temps = common_temps
    hums = common_hums

    illness_days = map_weather_to_historic_data(temps, hums)

    illness = IllnessCase.OIDIUM

    assert [
               IllnessConditEnc.NONE_CONDITION_SATISF,
               IllnessConditEnc.START_CONDITION_SATISF,
               IllnessConditEnc.NONE_CONDITION_SATISF,
               IllnessConditEnc.NONE_CONDITION_SATISF,
               IllnessConditEnc.OPTIMAL_CONDITION_SATISF,
           ] == illness_days.get_illness_historic_data(illness)
