import json

from algo_client import get_illness_prob_for_each_timeunit, get_illness_prob_for_each_timeunit_def
from illness_cases_spec import IllnessCase

file_path = 'test_response_hourly.json'


def open_test_file():
    data = None
    with open(file=file_path, mode='r') as file:
        data = file.read()
    return data


# temps, hums
def get_temps_and_hums_hourly() -> tuple[list[float], list[float]]:
    parsed_data = json.loads(open_test_file())
    temps = parsed_data[0]["weather"]["temperature_2m"]
    hums = parsed_data[0]["weather"]["relative_humidity_2m"]
    hums = list(map(lambda hum: hum / 100.0, hums))
    return temps, hums


def test_json_is_parsed():
    temps, hums = get_temps_and_hums_hourly()
    print(len(temps))

    assert len(temps) == 360 and len(hums) == 360


def test_get_illness_prob_for_each_timeunit():
    temps, hums = get_temps_and_hums_hourly()

    probs = get_illness_prob_for_each_timeunit_def(
        temps=temps,
        hums=hums,
        illness_name=IllnessCase.ALTERNARIOZ.name
    )

    print(probs)

    assert len(probs) > 0
