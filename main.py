import logging
import pygame

from Entities.Map.map import Map
from Entities.Unit.empire_trooper import EmpireKnight
from Entities.Unit.squad import Squad
from Entities.Unit.undead_trooper import SkeletonRider, Skeleton
from Enums.colors import COLORS
from settings import RESOLUTION_X, RESOLUTION_Y
from Enums.landscape import Landscape

logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    attack_squad = Squad([Skeleton(), SkeletonRider(), Skeleton()])
    defend_squad = Squad([EmpireKnight(), EmpireKnight(), EmpireKnight()])
    # attack_squad, defend_squad = CombatHandler(attack_squad, defend_squad).execute_combat()

    map_tiles_x, map_tiles_y = 50, 50
    map = Map(map_tiles_x, map_tiles_y)
    print(map)
    print(map.get_tile_by_cors(2, 3))

    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([RESOLUTION_Y, RESOLUTION_X])

    # Run until the user asks to quit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill((255, 255, 255))

        single_tile_diameter = int(RESOLUTION_Y / map_tiles_y)
        for tile in map:
            pygame.draw.circle(
                screen,
                COLORS["blue"].rgb_tuple
                if tile.terrain.landscape == Landscape.PLAINS
                else COLORS["green"].rgb_tuple,
                (single_tile_diameter * tile.x_cor, single_tile_diameter * tile.y_cor),
                single_tile_diameter / 2,
            )

        # Flip the display
        pygame.display.flip()

    pygame.quit()
