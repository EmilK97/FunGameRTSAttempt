import logging
import random
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

    while running:
        # Fill the background with white
        draw_map(map, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                for attacker_squad in WarlordAttacker.squads:
                    attacker_squad.move_to_tile(
                        map.get_tile_by_cors(random.randint(0, 5), random.randint(0, 8))
                    )
                    if defender_squad := is_squad_overlapping_with_any_of_squads(
                            attacker_squad, WarlordDefender.squads
                    ):
                        CombatHandler(
                            attacker_squad,
                            WarlordAttacker,
                            defender_squad,
                            WarlordDefender,
                        ).execute_combat()

        draw_squads(map, screen, WarlordAttacker.squads)
        draw_squads(map, screen, WarlordDefender.squads)

        FPS.tick(FSP_LIMIT)
        pygame.display.update()

    pygame.quit()
