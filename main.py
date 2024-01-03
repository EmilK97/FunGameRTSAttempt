import logging
from typing import Optional

import pygame

from Engine.combat import CombatHandler
from Engine.draw import draw_map, draw_squads
from Entities.Map.map import Map
from Entities.Unit.empire_trooper import EmpireKnight
from Entities.Unit.squad import Squad
from Entities.Unit.undead_trooper import SkeletonRider, Skeleton
from Entities.Warlord.warlord import Warlord
from settings import RESOLUTION_X, RESOLUTION_Y, FSP_LIMIT

logging.basicConfig(level=logging.DEBUG)


def is_squad_overlapping_with_any_of_squads(
    squad: Squad, squads_to_check: list[Squad]
) -> Optional[Squad]:
    for squad_to_check in squads_to_check:
        if squad_to_check.tile_location == squad.tile_location:
            return squad_to_check


if __name__ == "__main__":
    WarlordAttacker = Warlord("Attacker")
    WarlordDefender = Warlord("Defender")
    map = Map(9, 16)

    WarlordAttacker.add_squad(
        Squad(
            Skeleton(),
            starting_tile=map.get_tile_by_cors(3, 8),
        )
    )
    WarlordAttacker.add_squad(
        Squad(
            Skeleton(),
            SkeletonRider(),
            Skeleton(),
            starting_tile=map.get_tile_by_cors(5, 1),
        )
    )
    WarlordDefender.add_squad(
        Squad(
            EmpireKnight(),
            EmpireKnight(),
            EmpireKnight(),
            starting_tile=map.get_tile_by_cors(0, 0),
        )
    )

    pygame.init()
    FPS = pygame.time.Clock()
    screen = pygame.display.set_mode([RESOLUTION_Y, RESOLUTION_X])
    running = True
    chosen_squad: Optional[Squad] = None

    while running:
        # Fill the background with white
        draw_map(map, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # left click
                    clicked_tile = map.get_tile_py_px_click(event.pos[0], event.pos[1])
                    print(clicked_tile)
                    if chosen_squad is None:
                        for squad in WarlordAttacker.squads:
                            if squad.tile_location == clicked_tile:
                                chosen_squad = squad
                                break
                        else:
                            chosen_squad = None
                    else:
                        chosen_squad.move_to_tile(clicked_tile)
                        if defender_squad := is_squad_overlapping_with_any_of_squads(
                            chosen_squad, WarlordDefender.squads
                        ):
                            CombatHandler(
                                chosen_squad,
                                WarlordAttacker,
                                defender_squad,
                                WarlordDefender,
                            ).execute_combat()
                        chosen_squad = None
                    print(f"Chosen squad: {chosen_squad}")

                if event.button == 3:  # right click
                    clicked_tile = map.get_tile_py_px_click(event.pos[0], event.pos[1])
                    print(clicked_tile)
                    for squad in WarlordAttacker.squads + WarlordDefender.squads:
                        if squad.tile_location == clicked_tile:
                            print(f"Squad info: {squad}")

            if event.type == pygame.KEYDOWN:
                print(f"Chosen squad: {chosen_squad}")

        draw_squads(map, screen, WarlordAttacker.squads + WarlordDefender.squads)
        FPS.tick(FSP_LIMIT)
        pygame.display.update()

    pygame.quit()
