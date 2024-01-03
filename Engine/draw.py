import pygame

from Entities.Map.map import Map
from Entities.Unit.squad import Squad
from Enums.colors import BLUE, GREEN, WHITE
from Enums.landscape import Landscape


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
