import argparse
import dataclasses
import json
import sys
from time import sleep
from typing import Dict, Optional, Tuple

from dacite import from_dict


sys.path.append("../")

from client.bench import run_benchmarks
from client.members import MEMBERS
from client.engine import clear, get_engine_exe, pull_engine
from client.games import CutechessMan, MatchResult


import requests
from common.spsa import Param

from common.utils import GameRequest, SpsaInfo, TestRequest


def get_spsa_params(
    params: Dict[str, Param], delta: Dict[str, float]
) -> Tuple[Dict[str, int], Dict[str, int]]:
    params_a = {}
    params_b = {}
    for name, param in params.items():
        params_a[name] = round(
            max(min(param.value + delta[name], param.highest), param.lowest)
        )
        params_b[name] = round(
            max(min(param.value - delta[name], param.highest), param.lowest)
        )
    return params_a, params_b


def game_count(threads: int):
    if threads % 2 == 1:
        threads += 1
    return threads


def get_test(server: str) -> Optional[GameRequest]:
    test = requests.get(f"{server}/get")
    if len(test.content) == 0:
        return None
    return from_dict(data_class=GameRequest, data=test.json())


def setup_engine(name: str, branch: str) -> Optional[str]:
    engine = MEMBERS[name]
    pull_engine(engine.repo)
    return get_engine_exe(name, branch, engine.make_dir)


def play_games(game_request: GameRequest, threads: int) -> Optional[MatchResult]:
    engine = setup_engine(game_request.engine, game_request.branch)
    if engine is None:
        return None

    nps = run_benchmarks(engine, threads)
    if nps == 0:
        return None
    scaled_tc = game_request.tc * MEMBERS[game_request.engine].nps / nps
    cutechess = CutechessMan(
        engine,
        game_request.book,
        game_count(threads),
        scaled_tc,
        game_request.hash_size,
        threads,
    )
    params_a, params_b = get_spsa_params(game_request.params, game_request.delta)
    return cutechess.run(params_a, params_b)


def client_run(server: str, threads: int) -> bool:
    game_request = get_test(server)
    if game_request is None:
        return False
    match_result = play_games(game_request, threads)
    if match_result is None:
        return False
    spsa_info = SpsaInfo(
        game_request.test_id,
        game_request.delta,
        match_result.w,
        match_result.l,
        match_result.d,
    )
    as_json = json.dumps(dataclasses.asdict(spsa_info))
    requests.post(f"{server}/result", json=as_json)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Open Tune Client",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Required
    parser.add_argument("--server", type=str, required=True, help="server link")
    parser.add_argument("--threads", type=int, required=True, help="thread count")
    parser.add_argument("--no-clear", action="store_true", help="whether to clear ")

    args = parser.parse_args()
    try:
        while True:
            if not client_run(args.server, args.threads):
                sleep(5)
    finally:
        if not args.no_clear:
            clear()


if __name__ == "__main__":
    # params = {"fp_margin": Param(100.0, 50.0, 150.0, 10.0)}
    # test = TestRequest("test", "blackmarlin", "tune", 8, "4moves_noob.epd", 8, params)

    # requests.post(f"http://127.0.0.1:5000/test", json=json.dumps(dataclasses.asdict(test)))
    main()
