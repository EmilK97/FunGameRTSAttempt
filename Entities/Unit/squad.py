import logging

import pygame
from pygame import Surface

from Entities.Map.map import Map
from Entities.Map.tile import Tile
from settings import SQUAD_ICON


class Squad(list, pygame.sprite.Sprite):
    pass

    def __init__(self, *args, starting_tile: Tile):
        super().__init__(args)
        self._tile_location = starting_tile
        self.image = pygame.image.load(SQUAD_ICON)
        self.rect = self.image.get_rect()

    def draw(self, surface: Surface, map: Map):
        self.rect.center = map.get_tile_px_placement(self._tile_location)
        surface.blit(self.image, self.rect)

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
