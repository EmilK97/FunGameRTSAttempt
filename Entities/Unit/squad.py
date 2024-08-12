import logging

import pygame
from Entities.Map.tile import Tile
from Enums.exceptions import SquadSizeLimitReach
from settings import SQUAD_ICON


class Squad(list, pygame.sprite.Sprite):
    SIZE_LIMIT = 8

    def __init__(self, *args, starting_tile: Tile, image_path: str = SQUAD_ICON):
        super().__init__(args)
        self._tile_location = starting_tile
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def move_to_tile(self, new_tile: Tile):
        if new_tile:
            self._tile_location = new_tile
        else:
            logging.warning(f"Failed to move - tile out of map range f{str(self)}")

    @property
    def tile_location(self) -> Tile:
        return self._tile_location

    def __str__(self):
        return f"Location: {self._tile_location}, units: {[str(_) for _ in self]}"

    def append(self, __object):
        if len(self) >= self.SIZE_LIMIT:
            raise SquadSizeLimitReach
        super().append(__object)


class Garnison(Squad):
    SIZE_LIMIT = 16
