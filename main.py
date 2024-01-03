import logging
import pygame

from Entities.Map.map import Map
from Entities.Unit.empire_trooper import EmpireKnight
from Entities.Unit.squad import Squad
from Entities.Warlord.warlord import Warlord
from Entities.Unit.undead_trooper import SkeletonRider, Skeleton
from Enums.colors import BLUE, RED, GREEN, WHITE
from settings import RESOLUTION_X, RESOLUTION_Y, FSP_LIMIT
from Enums.landscape import Landscape
from Engine.combat import CombatHandler
import random

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    WarlordAttacker = Warlord("Attacker")
    WarlordDefender = Warlord("Defender")
    map_tiles_x, map_tiles_y = 10, 10
    map = Map(map_tiles_x, map_tiles_y)

    WarlordAttacker.add_squad(
        Squad(
            Skeleton(),
            SkeletonRider(),
            Skeleton(),
            starting_tile=map.get_tile_by_cors(0, 1),
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

    # Set up the drawing window
    screen = pygame.display.set_mode([RESOLUTION_Y, RESOLUTION_X])

    # Run until the user asks to quit
    running = True
    while running:
        # Fill the background with white
        screen.fill(WHITE)

        for tile in map:
            pygame.draw.circle(
                screen,
                BLUE if tile.terrain.landscape == Landscape.PLAINS else GREEN,
                map.get_tile_px_placement(tile),
                Map.TILE_RADIUS_PX,
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                WarlordAttacker.squads[0].move_to_tile(
                    map.get_tile_by_cors(0, random.randint(0, 8))
                )
                for defender_squad in WarlordDefender.squads:
                    if (
                        WarlordAttacker.squads[0].tile_location
                        == defender_squad.tile_location
                    ):
                        CombatHandler(
                            WarlordAttacker.squads[0], WarlordDefender.squads[0]
                        ).execute_combat()
                    if not defender_squad:
                        WarlordDefender.remove_squad(defender_squad)

            if event.type == pygame.MOUSEWHEEL:
                pygame.draw.circle(
                    screen,
                    RED,
                    (200, 200),
                    100,
                )

        [squad.draw(screen, map) for squad in WarlordAttacker.squads]
        [squad.draw(screen, map) for squad in WarlordDefender.squads]
        # Flip the display
        FPS.tick(FSP_LIMIT)
        pygame.display.flip()

    pygame.quit()
