from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Param:
    value: float
    lowest: float
    highest: float
    step: float


@dataclass
class SpsaParam:
    max_iter: int
    a: float = 1.0
    c: float = 1.0
    A: float = 100000
    alpha: float = 0.601
    gamma: float = 0.102


@dataclass
class SpsaTest:
    test_id: str
    engine: str
    branch: str
    book: str
    hash_size: int
    tc: float


@dataclass
class SpsaTuner:
    config: SpsaTest
    spsa_params: SpsaParam
    engine_params: Dict[str, Param]
    t: int
    iters: List[int]
    hist: Dict[str, List[float]]
