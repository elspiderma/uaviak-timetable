import os
from typing import Tuple


def parse_massive_int_env(name: str, sep: str = ',') -> Tuple[int]:
    """ Парсит массив значений типа int из переменой окружения.

    @param name: Имя переменой окружения.
    @param sep: Разделитель между элементами.
    @return: Кортеж из элементов.
    """
    varenv = os.getenv(name)
    if varenv is None:
        return tuple()

    varenv_split = varenv.split(sep)
    varenv_split = tuple(varenv_split)
    varenv_split = tuple(map(int, varenv_split))  # Convert ('123', '345') to (123, 345)
    return varenv_split
