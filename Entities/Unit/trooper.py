from abc import ABC
from Enums.races import Races
from Enums.factions import Factions
from random import randint
from Entities.Skill.skill import Skill

import logging


class Trooper(ABC):
    name: str
    strength: int
    _max_hp: int
    _current_hp: int
    faction: Factions
    race: Races
    id: int
    speed: int
    primary_skill: Skill
    secondary_skill: Skill
    graphic: str  # .PNG file path

    def __init__(self, strength: int, max_hp: int, race: Races, name: str):
        self.id = randint(1, 2**16)
        self.name = name
        self.strength = strength
        self.race = race
        self._max_hp = max_hp
        self._current_hp = self._max_hp

    def __str__(self):
        return f"{self.name}, id: {self.id}, HP: {self.current_hp}/{self._max_hp}"

    @property
    def current_hp(self) -> int:
        return self._current_hp

    @current_hp.setter
    def current_hp(self, new_value: int):
        self._current_hp = new_value
        if self.current_hp < 1:
            self.die()

    @property
    def is_dead(self) -> bool:
        return False if self.current_hp > 0 else True

    def die(self):
        logging.info(f"{str(self)} is DEAD!!!\n")
        del self
