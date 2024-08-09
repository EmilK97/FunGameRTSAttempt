import pygame

from Entities.City.city import City
from Entities.Map.map import Map
from Entities.Unit.squad import Squad
from Enums.colors import GREY


def draw_map(map: Map, surface: pygame.Surface):
    surface.fill(GREY)
    for tile in map:
        tile.draw(surface, map)


def draw_squads(map: Map, surface: pygame.Surface, squads: list[Squad]):
    [squad.draw(surface, map) for squad in squads]


def draw_cities(map: Map, surface: pygame.Surface, cities: list[City]):
    [city.draw(surface, map) for city in cities]
