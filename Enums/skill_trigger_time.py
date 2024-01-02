from enum import Enum


class SkillTriggerTime(Enum):
    NONE = 0
    ON_DAMAGE = 1
    ON_ROUND_START = 2
    IN_CITY = 3
    OTHER = 4
