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
from Engine.movement.pathing import find_movement_path
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
    chosen_squad: Optional[Squad] = None
    chosen_path: Optional[tuple[Tile, ...]] = None

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
        if chosen_squad is not None:
            highlight_chosen_squad(game_map, screen, chosen_squad)
        if chosen_path is not None:
            draw_path_highlight(
                surface=screen,
                game_map=game_map,
                starting_tile=chosen_squad.tile_location,
                path=chosen_path,
            )

        # HANDLE USER CLICK EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                clicked_tile = game_map.get_tile_by_px_click(event.pos[0], event.pos[1])
                print(clicked_tile)

                if event.button == 1:  # left click - ACTION
                    if chosen_squad is None:
                        for squad in human_squads:
                            if squad.tile_location == clicked_tile:
                                chosen_squad = squad
                                break
                        else:
                            chosen_squad = None
                            chosen_path = None
                    elif chosen_squad is not None and chosen_path is None:
                        chosen_path, movement_cost = find_movement_path(
                            starting_tile=chosen_squad.tile_location,
                            target_tile=clicked_tile,
                            game_map=game_map,
                        )
                        break

                    elif chosen_squad is not None and chosen_path is not None:
                        movement_path, _ = find_movement_path(
                            starting_tile=chosen_squad.tile_location,
                            target_tile=clicked_tile,
                            game_map=game_map,
                        )
                        if movement_path == chosen_path:
                            # Player confirms by double-clicking target file with drawn path.
                            handle_squad_move_attempt(
                                squad_to_move=chosen_squad,
                                inactive_warlord=ai_warlord,
                                moving_squad_warlord=human_warlord,
                                target_tile=clicked_tile,
                                game_map=game_map,
                            )
                            chosen_squad = None
                            chosen_path = None
                        else:
                            # Player chose new path - re-draw.
                            chosen_path = movement_path

                if event.button == 3:  # right click - PRINT INFO
                    for squad in ai_squads + human_squads:
                        if squad.tile_location == clicked_tile:
                            print(f"Squad info: {squad}")
                    for city in game_map.cities:
                        if city.tile_location == clicked_tile:
                            print(f"City info: {city}")

            if event.type == pygame.KEYDOWN:
                print(f"Chosen squad: {chosen_squad}")

        FPS.tick(FSP_LIMIT)
        pygame.display.update()

        if kill_after_one_loop:
            #  Only True for smoke test.
            running = False

    if clear_temp_directory_on_game_end:
        clear_temp_directory()
    pygame.quit()
