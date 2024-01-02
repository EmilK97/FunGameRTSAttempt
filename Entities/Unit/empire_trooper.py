from Enums.races import Races
from Enums.factions import Factions
from Entities.Unit.trooper import Trooper
from abc import ABC


class EmpireTrooper(Trooper, ABC):
    def __init__(self, strength: int, max_hp: int, race: Races, name: str):
        super().__init__(strength, max_hp, race, name)
        self.faction = Factions.EMPIRE


class EmpireKnight(EmpireTrooper):
    def __init__(self):
        super().__init__(strength=10, max_hp=20, race=Races.HUMAN, name="Empire Knight")


class Swordsman(EmpireTrooper):
    def __init__(self):
        super().__init__(strength=7, max_hp=9, race=Races.HUMAN, name="Swordsman")
