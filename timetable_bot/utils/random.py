import random


def get_random() -> int:
    return random.getrandbits(31) * random.choice([-1, 1])
