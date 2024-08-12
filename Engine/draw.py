import pygame

from Entities.Map.map import Map
from Entities.Unit.squad import Squad
from Enums.colors import GREY


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
