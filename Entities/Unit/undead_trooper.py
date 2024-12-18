from Enums.races import Races
from Enums.factions import Factions
from Entities.Unit.trooper import Trooper
from abc import ABC

from Enums.trooper_type import TrooperType


class UndeadTrooper(Trooper, ABC):
    def __init__(
        self,
        strength: int,
        max_hp: int,
        race: Races,
        name: str,
        trooper_type: TrooperType,
    ):
        super().__init__(strength, max_hp, race, name, trooper_type)
        self.faction = Factions.UNDEAD


class SkeletonRider(UndeadTrooper):
    def __init__(self):
        super().__init__(
            strength=10,
            max_hp=20,
            race=Races.UNDEAD,
            name="Skeleton Rider",
            trooper_type=TrooperType.CAVALRY,
        )


class Skeleton(UndeadTrooper):
    def __init__(self):
        super().__init__(
            strength=6,
            max_hp=11,
            race=Races.UNDEAD,
            name="Skeleton",
            trooper_type=TrooperType.INFANTRY,
        )
