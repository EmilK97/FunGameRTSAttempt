import os

import attrs
import pygame

from Engine.graphics.process_image import resize_image, add_border_to_image
from Enums.landscape import Landscape
from settings import TERRAIN_SPRITES_PATH
from settings import TILE_IMAGE_SIZE_PX
from Enums.colors import GREEN


@attrs.define
class Terrain:
    landscape: Landscape
    movement_cost: int
    _texture_path: str

    @property
    def pygame_image(self):
        return pygame.image.load(self._texture_path)

    def __str__(self):
        return self.landscape.name


plains_image_path = add_border_to_image(
    resize_image(
        os.path.join(TERRAIN_SPRITES_PATH, "Plains.png"),
        TILE_IMAGE_SIZE_PX,
        TILE_IMAGE_SIZE_PX,
    )
)
PLAINS = Terrain(Landscape.PLAINS, 2, plains_image_path)
forest_image_path = add_border_to_image(
    resize_image(
        os.path.join(TERRAIN_SPRITES_PATH, "Forest.png"),
        TILE_IMAGE_SIZE_PX,
        TILE_IMAGE_SIZE_PX,
    ),
    rbg_color=GREEN,
)
FOREST = Terrain(Landscape.FOREST, 3, forest_image_path)
