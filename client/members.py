from ast import Str
from dataclasses import dataclass


@dataclass
class Engine:
    name: str
    repo: str
    make_dir: str
    nps: str


MEMBERS = {
    "blackmarlin": Engine(
        "blackmarlin", "https://github.com/dsekercioglu/blackmarlin", "./", 1500000
    )
}
