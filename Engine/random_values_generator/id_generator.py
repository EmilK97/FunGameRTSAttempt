from random import randint


def get_random_id() -> int:
    """Generate random int for id"""
    return randint(2**10, 2**32 - 1)
