import pygame

from Entities.Map.map import Map
from Entities.Unit.squad import Squad
from Enums.colors import GREY, YELLOW
from settings import TILE_IMAGE_SIZE_PX


def draw_map(map: Map, surface: pygame.Surface):
    surface.fill(GREY)
    for tile in map:
        tile.draw(surface, map)


def draw_squads(map: Map, surface: pygame.Surface, squads: list[Squad]):
    for squad in squads:
        squad.rect.center = map.get_tile_px_placement(squad.tile_location)
        surface.blit(squad.image, squad.rect)


def draw_cities(map: Map, surface: pygame.Surface):
    for city in map.cities:
        city.rect.center = map.get_tile_px_placement(city.tile_location)
        surface.blit(city.image, city.rect)


def highlight_chosen_squad(map: Map, surface: pygame.Surface, squad: Squad):
    """Draws a thin line under chosen squad to highlight."""
    x_pos_center, y_pos_center = map.get_tile_px_placement(squad.tile_location)
    px_tile_third_size = int(TILE_IMAGE_SIZE_PX / 3)
    pygame.draw.line(
        surface=surface,
        color=YELLOW,
        start_pos=[
            x_pos_center - px_tile_third_size,
            y_pos_center + px_tile_third_size,
        ],
        end_pos=[x_pos_center + px_tile_third_size, y_pos_center + px_tile_third_size],
        width=5,
    )
