from typing import Optional

import pygame

from Engine.combat import CombatHandler
from Engine.graphics.draw import (
    draw_map,
    draw_squads,
    draw_cities,
    highlight_chosen_squad,
)
from Entities.City.city import City
from Entities.Map.map import Map
from Entities.Map.tile import Tile
from Entities.Unit.squad import Squad
from Entities.Warlord.warlord import Warlord
from settings import RESOLUTION_X, RESOLUTION_Y, FSP_LIMIT


def is_tile_overlapping_with_any_of_squads(
    tile: Tile, squads_to_check: list[Squad]
) -> Optional[Squad]:
    for squad_to_check in squads_to_check:
        if squad_to_check.tile_location == tile:
            return squad_to_check


def is_tile_overlapping_with_any_of_cities(
    tile: Tile, cities_to_check: list[City]
) -> Optional[City]:
    for city_to_check in cities_to_check:
        if city_to_check.tile_location == tile:
            return city_to_check


def handle_squad_move_attempt(
    target_tile: Tile,
    squad_to_move: Squad,
    ai_warlord: Warlord,
    human_warlord: Warlord,
    all_cities_on_map: list[City],
):
    """Checks collision with other entites, if target tile already occupied.
    Initialize combat if target tile occupied by enemy squad, initalizes siege if tile occupied by enemy city, joins
    garrison if target tile is player city."""
    # Check if collides with enemy squad - should initiate field combat.
    if defender_squad := is_tile_overlapping_with_any_of_squads(
        target_tile, ai_warlord.squads
    ):
        has_squad_to_move_won = CombatHandler(
            attacker_squad=squad_to_move,
            attacker_warlord=human_warlord,
            defender_squad=defender_squad,
            defender_warlord=ai_warlord,
        ).execute_field_combat()
        if has_squad_to_move_won:
            squad_to_move.move_to_tile(target_tile)

    # Check if collides with player squad - should joins squad or fail if size toto big.
    elif is_tile_overlapping_with_any_of_squads(target_tile, human_warlord.squads):
        print("ERROR - merging squads not implemented!!")

    # Check if collides with any city:
    elif colliding_city := is_tile_overlapping_with_any_of_cities(
        target_tile, all_cities_on_map
    ):
        # Check if collides with enemy city - should initiate siege.
        if colliding_city in ai_warlord.cities:
            print("ERROR - attacking enemy cities not implemented.")

        # Check if collides with player City - should add to garrison.
        elif colliding_city in human_warlord.cities:
            print("ERROR - adding to garrison not implemented!!")
        # Else is a neutral city
        else:
            print("ERROR - attacking neutral cities not implemented.")

    else:  # Tile is free, move squad
        squad_to_move.move_to_tile(target_tile)


def main_game_loop(game_map: Map, human_warlord: Warlord, ai_warlord: Warlord):
    """For now assume single player, and human player is the first warlord from tuple."""

    pygame.init()
    FPS = pygame.time.Clock()
    screen = pygame.display.set_mode([RESOLUTION_Y, RESOLUTION_X])
    running = True
    chosen_squad: Optional[Squad] = None

    while running:
        human_squads = human_warlord.squads
        ai_squads = ai_warlord.squads
        all_squads = human_squads + ai_squads

        # DRAW MAP
        draw_map(game_map, screen)
        draw_squads(game_map, screen, all_squads)
        draw_cities(game_map, screen)
        if chosen_squad is not None:
            highlight_chosen_squad(game_map, screen, chosen_squad)

        # HANDLE USER CLICK EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                clicked_tile = game_map.get_tile_py_px_click(event.pos[0], event.pos[1])
                print(clicked_tile)

                if event.button == 1:  # left click - ACTION
                    if chosen_squad is None:
                        for squad in human_squads:
                            if squad.tile_location == clicked_tile:
                                chosen_squad = squad
                                break
                        else:
                            chosen_squad = None

                    elif chosen_squad is not None:
                        handle_squad_move_attempt(
                            squad_to_move=chosen_squad,
                            ai_warlord=ai_warlord,
                            human_warlord=human_warlord,
                            target_tile=clicked_tile,
                            all_cities_on_map=game_map.cities,
                        )
                        chosen_squad = None

                if event.button == 3:  # right click - PRINT INFO
                    for squad in all_squads:
                        if squad.tile_location == clicked_tile:
                            print(f"Squad info: {squad}")
                    for city in game_map.cities:
                        if city.tile_location == clicked_tile:
                            print(f"City info: {city}")

            if event.type == pygame.KEYDOWN:
                print(f"Chosen squad: {chosen_squad}")

        FPS.tick(FSP_LIMIT)
        pygame.display.update()

    pygame.quit()
