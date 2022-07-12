import json
import sys

from dacite import from_dict

sys.path.append("../")

import dataclasses
import requests
from common.spsa import Param

from common.utils import GameRequest, SpsaInfo, TestRequest


def get_spsa_params(params: dict[str, Param], delta: dict[str, float]) -> tuple[dict[str, int], dict[str, int]]:
    params_a = {}
    params_b = {}
    for name, param in params.items():
        params_a[name] = round(
            max(min(param.value + delta[name], param.highest), param.lowest))
        params_b[name] = round(
            max(min(param.value - delta[name], param.highest), param.lowest))
    return params_a, params_b

def main():
    local_host = "http://127.0.0.1:5000"

    params = {"fp_margin": Param(100.0, 50.0, 150.0, 10.0)}
    test = TestRequest("test", "blackmarlin", "tune", 8, "placeholder", 8, params)

    requests.post(f"{local_host}/test", json=json.dumps(dataclasses.asdict(test)))

    test = requests.get(f"{local_host}/get").json()
    test = from_dict(data_class=GameRequest, data=test)
    print(test)

    for _ in range(1000):
        spsa_info = SpsaInfo(test.test_id, test.delta, 2, 0, 0)
        requests.post(f"{local_host}/result", json=json.dumps(dataclasses.asdict(spsa_info)))
    params = requests.get(f"{local_host}/params/test").json()
    print(params)


if __name__ == "__main__":
    main()
