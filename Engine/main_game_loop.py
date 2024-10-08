from typing import Optional

import pygame

from Engine.combat import FieldCombatHandler, CitySiegeHandler
from Engine.graphics.draw import (
    draw_map,
    draw_squads,
    draw_cities,
    highlight_chosen_squad,
)
from Engine.graphics.process_image import clear_temp_directory
from Entities.City.city import City
from Entities.Map.gamemap import GameMap
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
    moving_squad_warlord: Warlord,
    inactive_warlord: Warlord,
    all_cities_on_map: list[City],
):
    """Checks collision with other entities, if target tile already occupied.
    Initialize combat if target tile occupied by enemy [opposing warlord's] squad, initializes siege if tile occupied by
    enemy [opposition's warlord] city, joins garrison if target tile is friendly city.
    """
    # Check if collides with enemy squad - should initiate field combat.
    if defender_squad := is_tile_overlapping_with_any_of_squads(
        target_tile, inactive_warlord.squads
    ):
        has_squad_to_move_won = FieldCombatHandler(
            attacker_squad=squad_to_move,
            defender_squad=defender_squad,
            terrain=target_tile.terrain,
        ).execute_field_combat()
        if has_squad_to_move_won:
            inactive_warlord.remove_squad(defender_squad)
            squad_to_move.move_to_tile(target_tile)
        else:
            # If squad to move lost, remove it from list.
            moving_squad_warlord.remove_squad(squad_to_move)

    # Check if collides with player squad - should joins squad or fail if size toto big.
    elif is_tile_overlapping_with_any_of_squads(
        target_tile, moving_squad_warlord.squads
    ):
        print("ERROR - merging squads not implemented!!")

    # Check if collides with any city:
    elif colliding_city := is_tile_overlapping_with_any_of_cities(
        target_tile, all_cities_on_map
    ):
        # Check if collides with enemy city - should initiate siege.
        if colliding_city in inactive_warlord.cities:
            has_squad_to_move_won = CitySiegeHandler(
                attacker_squad=squad_to_move, defender_city=colliding_city
            ).execute_city_siege()
            if has_squad_to_move_won:
                # If Squad won, warlords gain city, other warlord loses city.
                # squad_to_move.move_to_tile(target_tile)
                inactive_warlord.lose_city(colliding_city)
                moving_squad_warlord.gain_city(colliding_city)
            else:
                # If squad to move lost, remove it from list.
                moving_squad_warlord.remove_squad(squad_to_move)

        # Check if collides with player City - should add to garrison.
        elif colliding_city in moving_squad_warlord.cities:
            print("ERROR - adding to garrison not implemented!!")
        # Else is a neutral city
        else:
            has_squad_to_move_won = CitySiegeHandler(
                attacker_squad=squad_to_move, defender_city=colliding_city
            ).execute_city_siege()
            if has_squad_to_move_won:
                # If Squad won, warlords gain city.
                moving_squad_warlord.gain_city(colliding_city)
            else:
                # If squad to move lost, remove it from list.
                moving_squad_warlord.remove_squad(squad_to_move)

    else:  # Tile is free, move squad
        squad_to_move.move_to_tile(target_tile)


def main_game_loop(
    game_map: GameMap,
    human_warlord: Warlord,
    ai_warlord: Warlord,
    kill_after_one_loop=False,
    clear_temp_dircetory_on_game_end=True,
):
    """For now assume single player, and human player is the first warlord from tuple."""

    pygame.init()
    FPS = pygame.time.Clock()
    screen = pygame.display.set_mode([RESOLUTION_Y, RESOLUTION_X])
    running = True
    chosen_squad: Optional[Squad] = None

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

                    elif chosen_squad is not None:
                        handle_squad_move_attempt(
                            squad_to_move=chosen_squad,
                            inactive_warlord=ai_warlord,
                            moving_squad_warlord=human_warlord,
                            target_tile=clicked_tile,
                            all_cities_on_map=game_map.cities,
                        )
                        chosen_squad = None

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

    if clear_temp_dircetory_on_game_end:
        clear_temp_directory()
    pygame.quit()
