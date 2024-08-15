import pygame

from Engine.graphics.process_image import add_border_to_image
from Entities.City.city import City
from Entities.Map.gamemap import GameMap
from Entities.Unit.squad import Squad
from Enums.colors import GREY, YELLOW
from settings import TILE_IMAGE_SIZE_PX, CITY_ICON


def draw_map(game_map: GameMap, surface: pygame.Surface):
    surface.fill(GREY)
    for tile in game_map:
        tile.draw(surface, game_map)


def draw_squads(game_map: GameMap, surface: pygame.Surface, squads: list[Squad]):
    for squad in squads:
        squad.rect.center = game_map.get_tile_px_placement(squad.tile_location)
        surface.blit(squad.image, squad.rect)


def draw_cities(
    *,
    game_map: GameMap,
    surface: pygame.Surface,
    cities_boundary_color: dict[City : tuple[int]],
):
    """Draws all cities in map on a surface. cities_boundary_color indicates collection of cities for which specific
    color of boundary shall be added, like:
        {<City object>: (255, 0, 0)}, where key value is a tuple RGB color.
    """
    for city in game_map.cities:
        if city in cities_boundary_color:
            city.image = pygame.image.load(
                add_border_to_image(
                    CITY_ICON,
                    cities_boundary_color[city],
                    path_suffix=f"{str(cities_boundary_color[city])}_city_icon",
                )
            )

        city.rect.center = game_map.get_tile_px_placement(city.tile_location)
        surface.blit(city.image, city.rect)


def highlight_chosen_squad(game_map: GameMap, surface: pygame.Surface, squad: Squad):
    """Draws a thin line under chosen squad to highlight."""
    x_pos_center, y_pos_center = game_map.get_tile_px_placement(squad.tile_location)
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
