from typing import Optional

import pygame

from Engine.graphics.button import Button
from Engine.graphics.process_image import add_border_to_image
from Engine.movement.pathing import find_last_path_index_speed_allows_to_reach
from Entities.City.city import City
from Entities.Map.gamemap import GameMap
from Entities.Map.tile import Tile
from Entities.Unit.squad import Squad
from Enums.colors import GREY, YELLOW, DARKER_YELLOW
from settings import TILE_IMAGE_SIZE_PX, CITY_ICON, SQUAD_ICON


def draw_map(game_map: GameMap, surface: pygame.Surface):
    surface.fill(GREY)
    for tile in game_map:
        tile.draw(surface, game_map)


def draw_squads(
    game_map: GameMap,
    surface: pygame.Surface,
    squads: list[Squad],
    boundary_color: Optional[tuple[int]] = None,
):
    """Draws squads on a surface. squads_with_color indicates collection of squads to be drawn.
    Optionally include boundary color RGB tuple, if given a squad image with appropriate icon will be added to drawn
    instead."""
    for squad in squads:
        if boundary_color:
            squad.image = pygame.image.load(
                add_border_to_image(
                    SQUAD_ICON,
                    boundary_color,
                    path_suffix=f"{str(squad.id)}_squad_icon",
                )
            )
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


def draw_path_line_between_tiles(
    surface: pygame.Surface,
    game_map: GameMap,
    start_tile: Tile,
    next_tile: Tile,
    color: tuple[int, int, int],
):
    x_pos_start, y_pos_start = game_map.get_tile_px_placement(start_tile)
    x_pos_next, y_pos_next = game_map.get_tile_px_placement(next_tile)
    pygame.draw.line(
        surface=surface,
        color=color,
        start_pos=[x_pos_start, y_pos_start],
        end_pos=[x_pos_next, y_pos_next],
        width=8,
    )


def draw_path_highlight(
    surface: pygame.Surface,
    game_map: GameMap,
    starting_tile: Tile,
    path: tuple[Tile, ...],
    highlighted_squad_speed: int,
):
    if len(path) == 0:
        return

    max_tile_range_index = find_last_path_index_speed_allows_to_reach(
        highlighted_squad_speed, path
    )
    if len(path) == 1 and max_tile_range_index is not None:
        max_tile_range_index = 1

    if max_tile_range_index is None:
        max_tile_range_index = 0

    # Draw remaining lines for tiles in path
    draw_path_line_between_tiles(
        surface,
        game_map,
        starting_tile,
        next_tile=path[0],
        color=DARKER_YELLOW if max_tile_range_index > 0 else GREY,
    )
    for tile_index in range(len(path) - 1):
        color = DARKER_YELLOW if tile_index < max_tile_range_index else GREY
        draw_path_line_between_tiles(
            surface, game_map, path[tile_index], path[tile_index + 1], color=color
        )


def draw_buttons(
    surface: pygame.Surface,
    mouse_position: tuple[int, int],
    buttons: tuple[Button, ...],
):
    for button in buttons:
        # Button hover effect
        if button.rect.collidepoint(mouse_position):
            pygame.draw.rect(surface, button.hover_color, button.rect)
        else:
            pygame.draw.rect(surface, button.button_color, button.rect)

        # Draw button text
        text_rect = button.button_text.get_rect(center=button.rect.center)
        surface.blit(button.button_text, text_rect)
