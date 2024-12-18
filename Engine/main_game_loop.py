from typing import Optional

import pygame

from Engine.graphics.draw import (
    draw_map,
    draw_squads,
    draw_cities,
    highlight_chosen_squad,
    draw_path_highlight,
)
from Engine.graphics.process_image import clear_temp_directory
from Engine.movement.movement import handle_squad_move_attempt
from Engine.movement.pathing import (
    find_movement_path,
    find_last_path_index_speed_allows_to_reach,
)
from Entities.City.city import City
from Entities.Map.gamemap import GameMap
from Entities.Map.tile import Tile
from Entities.Unit.squad import Squad
from Entities.Warlord.warlord import Warlord
from settings import RESOLUTION_X, RESOLUTION_Y, FSP_LIMIT


def main_game_loop(
    game_map: GameMap,
    human_warlord: Warlord,
    ai_warlord: Warlord,
    kill_after_one_loop=False,
    clear_temp_directory_on_game_end=True,
):
    """For now assume single player, and human player is the first warlord from tuple."""

    pygame.init()
    FPS = pygame.time.Clock()
    screen = pygame.display.set_mode([RESOLUTION_Y, RESOLUTION_X])
    running = True
    HIGHLIGHTED_SQUAD: Optional[Squad] = None
    HIGHLIGHTED_PATH: Optional[tuple[Tile, ...]] = None

    while running:
        # DRAW MAP
        draw_map(game_map, screen)

        # DRAW SQUADS
        human_squads = human_warlord.squads
        draw_squads(game_map, screen, human_squads, human_warlord.color)

        ai_squads = ai_warlord.squads
        draw_squads(game_map, screen, ai_squads, ai_warlord.color)

        # DRAW CITIES
        cities_boundary_color: dict[City, tuple[int]] = dict()
        [
            cities_boundary_color.update({city: human_warlord.color})
            for city in human_warlord.cities
        ]
        [
            cities_boundary_color.update({city: ai_warlord.color})
            for city in ai_warlord.cities
        ]
        draw_cities(
            game_map=game_map,
            surface=screen,
            cities_boundary_color=cities_boundary_color,
        )

        if HIGHLIGHTED_SQUAD is not None:
            highlight_chosen_squad(game_map, screen, HIGHLIGHTED_SQUAD)
            if HIGHLIGHTED_PATH is not None:
                draw_path_highlight(
                    surface=screen,
                    game_map=game_map,
                    starting_tile=HIGHLIGHTED_SQUAD.tile_location,
                    path=HIGHLIGHTED_PATH,
                    highlighted_squad_speed=HIGHLIGHTED_SQUAD.speed,
                )

        # HANDLE USER CLICK EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                clicked_tile = game_map.get_tile_by_px_click(event.pos[0], event.pos[1])

                if event.button == 1:  # left click - ACTION
                    if HIGHLIGHTED_SQUAD is None:
                        for squad in human_squads:
                            if squad.tile_location == clicked_tile:
                                HIGHLIGHTED_SQUAD = squad
                                break
                        else:
                            HIGHLIGHTED_SQUAD = None
                            HIGHLIGHTED_PATH = None
                    elif HIGHLIGHTED_SQUAD is not None and HIGHLIGHTED_PATH is None:
                        HIGHLIGHTED_PATH = find_movement_path(
                            starting_tile=HIGHLIGHTED_SQUAD.tile_location,
                            target_tile=clicked_tile,
                            game_map=game_map,
                        )
                        break

                    elif HIGHLIGHTED_SQUAD is not None and HIGHLIGHTED_PATH is not None:
                        movement_path = find_movement_path(
                            starting_tile=HIGHLIGHTED_SQUAD.tile_location,
                            target_tile=clicked_tile,
                            game_map=game_map,
                        )
                        if movement_path == HIGHLIGHTED_PATH:
                            # Player confirms by double-clicking target file with drawn path.
                            handle_squad_move_attempt(
                                squad_to_move=HIGHLIGHTED_SQUAD,
                                inactive_warlord=ai_warlord,
                                moving_squad_warlord=human_warlord,
                                path=HIGHLIGHTED_PATH,
                                game_map=game_map,
                            )
                            HIGHLIGHTED_SQUAD = None
                            HIGHLIGHTED_PATH = None
                        else:
                            # Player chose new path - re-draw.
                            HIGHLIGHTED_PATH = movement_path

                if event.button == 3:  # right click
                    # Cancel highlighted squad and path.
                    HIGHLIGHTED_PATH = None
                    HIGHLIGHTED_SQUAD = None
                    # PRINT INFO of clicked field.
                    for squad in ai_squads + human_squads:
                        if squad.tile_location == clicked_tile:
                            print(f"Squad info: {squad}")
                    for city in game_map.cities:
                        if city.tile_location == clicked_tile:
                            print(f"City info: {city}")

                    print(clicked_tile)

            if event.type == pygame.KEYDOWN:
                print(f"Chosen squad: {HIGHLIGHTED_SQUAD}")

        FPS.tick(FSP_LIMIT)
        pygame.display.update()

        if kill_after_one_loop:
            #  Only True for smoke test.
            running = False

    if clear_temp_directory_on_game_end:
        clear_temp_directory()
    pygame.quit()
