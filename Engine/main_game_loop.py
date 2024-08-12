from typing import Optional

import pygame

from Engine.combat import CombatHandler
from Engine.graphics.draw import draw_map, draw_squads, draw_cities
from Entities.Map.map import Map
from Entities.Unit.squad import Squad
from Entities.Warlord.warlord import Warlord
from settings import RESOLUTION_X, RESOLUTION_Y, FSP_LIMIT


def is_squad_overlapping_with_any_of_squads(
    squad: Squad, squads_to_check: list[Squad]
) -> Optional[Squad]:
    for squad_to_check in squads_to_check:
        if squad_to_check.tile_location == squad.tile_location:
            return squad_to_check


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

        draw_map(game_map, screen)
        draw_squads(game_map, screen, all_squads)
        draw_cities(game_map, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # left click
                    clicked_tile = game_map.get_tile_py_px_click(
                        event.pos[0], event.pos[1]
                    )
                    print(clicked_tile)
                    if chosen_squad is None:
                        for squad in human_squads:
                            if squad.tile_location == clicked_tile:
                                chosen_squad = squad
                                break
                        else:
                            chosen_squad = None
                    else:
                        chosen_squad.move_to_tile(clicked_tile)
                        if defender_squad := is_squad_overlapping_with_any_of_squads(
                            chosen_squad, ai_squads
                        ):
                            CombatHandler(
                                chosen_squad, human_warlord, defender_squad, ai_warlord
                            ).execute_combat()
                        chosen_squad = None
                    print(f"Chosen squad: {chosen_squad}")

                if event.button == 3:  # right click
                    clicked_tile = game_map.get_tile_py_px_click(
                        event.pos[0], event.pos[1]
                    )
                    print(clicked_tile)
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
