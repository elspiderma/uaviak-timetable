import os
from typing import Tuple


def parse_massive_int_env(name: str, sep: str = ',') -> Tuple[int]:
    varenv = os.getenv(name)
    if varenv is None:
        return tuple()

    varenv_split = varenv.split(sep)
    varenv_split = tuple(varenv_split)
    varenv_split = tuple(map(int, varenv_split))  # Convert ('123', '345') to (123, 345)
    return varenv_split
