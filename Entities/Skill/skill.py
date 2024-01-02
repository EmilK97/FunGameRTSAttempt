from abc import ABC
from attr import attr, field
from Enums.skill_trigger_time import SkillTriggerTime


@attr
class Skill(ABC):
    skill_level: field(default=0)
    name: field(default="empty")
    triger_time: SkillTriggerTime

    def execute_skill(self):
        pass

    def __str__(self):
        return f"{self.name} of level {self.skill_level}"
