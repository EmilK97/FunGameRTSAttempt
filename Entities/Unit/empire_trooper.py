from abc import ABC

from Entities.Unit.trooper import Trooper
from Enums.factions import Factions
from Enums.races import Races
from Enums.trooper_type import TrooperType


class EmpireTrooper(Trooper, ABC):
    def __init__(
        self,
        strength: int,
        max_hp: int,
        race: Races,
        name: str,
        trooper_type: TrooperType,
    ):
        super().__init__(strength, max_hp, race, name, trooper_type)
        self.faction = Factions.EMPIRE


class EmpireKnight(EmpireTrooper):
    def __init__(self):
        super().__init__(
            strength=10,
            max_hp=20,
            race=Races.HUMAN,
            name="Empire Knight",
            trooper_type=TrooperType.CAVALRY,
        )


class Swordsman(EmpireTrooper):
    def __init__(self):
        super().__init__(
            strength=7,
            max_hp=9,
            race=Races.HUMAN,
            name="Swordsman",
            trooper_type=TrooperType.INFANTRY,
        )
