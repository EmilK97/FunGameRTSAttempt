from enum import Enum


class CityTier(Enum):
    OUTPOST = 1
    FORT = 2
    CITY = 3
    FORTIFIED_CITY = 4
    CAPITAL_CITY = 5

    def __int__(self):
        return int(self.value)
