from dataclasses import dataclass
from typing import Dict

from common.spsa import Param


@dataclass
class TestRequest:
    test_id: str
    engine: str
    branch: str
    hash_size: int
    book: str
    tc: float
    params: Dict[str, Param]
    max_iter: int = 1000000


@dataclass
class GameRequest:
    test_id: str
    engine: str
    branch: str
    book: str
    hash_size: int
    params: Dict[str, Param]
    delta: Dict[str, float]
    tc: float


@dataclass
class SpsaInfo:
    test_id: str
    delta: Dict[str, float]
    w: int
    l: int
    d: int