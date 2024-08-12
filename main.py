import logging
from typing import Optional

import pygame

from Engine.combat import CombatHandler
from Engine.draw import draw_map, draw_squads, draw_cities
from Entities.City.city import City
from Entities.Map.map import Map
from Entities.Map.tile import TileCoordinates
from Entities.Unit.empire_trooper import EmpireKnight
from Entities.Unit.squad import Squad
from Entities.Unit.undead_trooper import SkeletonRider, Skeleton
from Entities.Warlord.warlord import Warlord
from Enums.factions import Factions
from Enums.races import Races
from settings import RESOLUTION_X, RESOLUTION_Y, FSP_LIMIT
from Enums.colors import RED, PURPLE

logging.basicConfig(level=logging.DEBUG)


def is_squad_overlapping_with_any_of_squads(
    squad: Squad, squads_to_check: list[Squad]
) -> Optional[Squad]:
    for squad_to_check in squads_to_check:
        if squad_to_check.tile_location == squad.tile_location:
            return squad_to_check


if __name__ == "__main__":
    map = Map(
        x_length=9,
        y_length=16,
        for_amount_of_players=2,
        players_starting_coordinates_in_order=(
            TileCoordinates(5, 10),
            TileCoordinates(0, 0),
        ),
        neutral_cities_coordinates=(
            TileCoordinates(2, 2),
            TileCoordinates(6, 8),
        ),
    )

    WarlordAttacker = Warlord(
        "Attacker",
        color=PURPLE,
        capital_city_name="AttackCapital#1",
        favorite_faction=Factions.EMPIRE,
        favorite_race=Races.ELF,
    )
    WarlordDefender = Warlord(
        "Defender",
        color=RED,
        capital_city_name="DefCapital#1",
        favorite_race=Races.UNDEAD,
        favorite_faction=Factions.UNDEAD,
    )

    WarlordAttacker.add_squad(
        Squad(
            Skeleton(),
            starting_tile=map.get_tile_by_cors(3, 8),
        )
    )
    map.create_capital_cities(WarlordAttacker, WarlordDefender)

    WarlordAttacker.squads[0].append(Skeleton())
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
            starting_tile=map.get_tile_by_cors(0, 1),
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
                    for city in map.cities:
                        if city.tile_location == clicked_tile:
                            print(f"City info: {city}")

            if event.type == pygame.KEYDOWN:
                print(f"Chosen squad: {chosen_squad}")

        draw_squads(map, screen, WarlordAttacker.squads + WarlordDefender.squads)
        draw_cities(map, screen)
        FPS.tick(FSP_LIMIT)
        pygame.display.update()

    pygame.quit()
