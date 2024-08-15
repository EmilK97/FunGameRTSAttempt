import logging
from abc import ABC

from Engine.random_values_generator.id_generator import get_random_id
from Entities.Skill.skill import Skill
from Enums.factions import Factions
from Enums.races import Races


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
    primary_skill_level: int = 1
    secondary_skill: Skill
    secondary_skill_level: int = 0
    sprite: str  # .PNG file path

    def __init__(self, strength: int, max_hp: int, race: Races, name: str):
        self.id = get_random_id()
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

    def take_damage(self, damage: int):
        self._current_hp += -1 * damage
        if self.current_hp < 1:
            self.die()

    @property
    def is_dead(self) -> bool:
        return False if self.current_hp > 0 else True

    def die(self):
        logging.info(f"{str(self)} is DEAD!!!\n")
        del self
