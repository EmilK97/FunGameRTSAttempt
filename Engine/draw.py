import os.path

import pygame
from PIL import Image, ImageOps

from Entities.City.city import City
from Entities.Map.map import Map
from Entities.Unit.squad import Squad
from Enums.colors import BLUE, GREEN, WHITE, BLACK
from Enums.landscape import Landscape
from settings import TROOPER_SPRITES_PATH, SQUAD_BORDER_SIZE


def draw_map(map: Map, surface: pygame.Surface):
    surface.fill(WHITE)
    for tile in map:
        pygame.draw.circle(
            surface,
            BLUE if tile.terrain.landscape == Landscape.PLAINS else GREEN,
            map.get_tile_px_placement(tile),
            Map.TILE_RADIUS_PX,
        )


def draw_squads(map: Map, surface: pygame.Surface, squads: list[Squad]):
    [squad.draw(surface, map) for squad in squads]


def draw_cities(map: Map, surface: pygame.Surface, cities: list[City]):
    [city.draw(surface, map) for city in cities]


def add_border_to_image(
    image_path: str, rbg_color: tuple[int] = BLACK, path_suffix: str = ""
) -> str:
    """Returns path to newly saved image"""
    # new_path = os.path.join(TROOPER_SPRITES_PATH, f"_temp_{path_suffix}_{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}.png")
    new_path = os.path.join(TROOPER_SPRITES_PATH, f"_temp_{path_suffix}.png")
    img = Image.open(image_path)
    img_with_border = ImageOps.expand(img, border=SQUAD_BORDER_SIZE, fill=rbg_color)
    img_with_border.resize(img.size)
    img_with_border.save(new_path)

    return new_path
