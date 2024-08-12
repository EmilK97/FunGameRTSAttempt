import logging
from random import randint

import pygame
from Entities.Map.tile import Tile
from Enums.factions import Factions
from Enums.races import Races
from settings import CITY_ICON


class City(pygame.sprite.Sprite):
    name: str
    _max_hp: int
    _current_hp: int
    faction: Factions
    race: Races
    id: int
    tile_location: Tile
    image_path: str

    def __init__(
        self,
        *groups,
        race: Races,
        faction: Factions,
        name: str,
        tile_location: Tile,
        image_path: str = CITY_ICON,
    ):
        super().__init__(*groups)
        self.id = randint(1, 2**16)
        self.name = name
        self.race = race
        self.faction = faction
        self.tile_location = tile_location
        self._max_hp = 20
        self._current_hp = self._max_hp
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def __str__(self):
        return f"City {self.name}, id: {self.id}, HP: {self.current_hp}/{self._max_hp}"

    @property
    def current_hp(self) -> int:
        return self._current_hp

    @current_hp.setter
    def current_hp(self, new_value: int):
        self._current_hp = new_value
        if self.current_hp < 1:
            self.destroy()

    def destroy(self):
        logging.info(f"City {str(self)} was destroyed!!!\n")
        del self


class CapitalCity(City):
    def __str__(self):
        return f"Capital {super().__str__()}"
