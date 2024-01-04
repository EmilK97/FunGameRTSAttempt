import attrs
from Enums.skill_trigger_time import SkillTriggerTime


@attrs.define
class Skill:
    name: str
    trigger_time: SkillTriggerTime

    def execute_skill(self):
        pass

    def __str__(self):
        return f"{self.name}"


FIRE_SKILL = Skill(name="Fire", trigger_time=SkillTriggerTime.ON_DAMAGE)
