import enum
from mailbox import linesep
import os
import pathlib
import platform
from typing import Optional


def _cutechess_exe_name() -> str:
    system = platform.system()
    if system == "Windows":
        return "cutechess-cli.exe"
    else:
        return "cutechess-cli"


def get_cutechess() -> Optional[str]:
    exe_name = _cutechess_exe_name()
    cutechess_path = pathlib.Path("cutechess").joinpath(exe_name)
    if cutechess_path.exists():
        return cutechess_path
    print(
        "Make a cutechess folder inside the client folder and put the cutechess executable inside it",
        f"File name should be '{exe_name}'",
        sep=os.linesep,
    )
    return None


class OpeningBook(enum.Enum):
    NOOB_4_MOVES = "4moves_noob.epd"
    POHL = "Pohl.epd"


def get_book(book: OpeningBook) -> Optional[str]:
    books_path = pathlib.Path("book").joinpath(book.value)
    if books_path.exists():
        return books_path
    print(
        "Make a books folder inside the client folder and put the opening books inside it",
        f"Current used books are: {[book.value for book in OpeningBook]}",
        f"These books can be found on the OpenBench github repository",
        sep=os.linesep,
    )
    return None
