from random import randint


def get_random_id() -> int:
    """Generate random int for id"""
    return randint(2**8, 2**16 - 1)
