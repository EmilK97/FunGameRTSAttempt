import logging

from Engine.main_game_loop import main_game_loop
from Entities.City.city import City
from Entities.Map.NeutralCityTemplate import NeutralCityTemplate
from Entities.Map.gamemap import GameMap
from Entities.Map.tile import TileCoordinates
from Entities.Unit.empire_trooper import EmpireKnight
from Entities.Unit.squad import Squad, Garrison
from Entities.Unit.undead_trooper import SkeletonRider, Skeleton
from Entities.Warlord.warlord import Warlord
from Enums.city_tier import CityTier
from Enums.colors import RED, PURPLE
from Enums.factions import Factions
from Enums.races import Races

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    game_map = GameMap(
        x_length=9,
        y_length=16,
        for_amount_of_players=2,
        players_starting_coordinates_in_order=(
            TileCoordinates(5, 10),
            TileCoordinates(0, 0),
        ),
        neutral_cities_template=(
            NeutralCityTemplate(
                race=Races.UNDEAD,
                faction=Factions.UNDEAD,
                tile_coordinates=TileCoordinates(3, 3),
                name="Weak skeleton city",
                tier=CityTier.OUTPOST,
                garrison=(Skeleton(), Skeleton()),
            ),
            NeutralCityTemplate(
                race=Races.HUMAN,
                faction=Factions.EMPIRE,
                tile_coordinates=TileCoordinates(5, 5),
                name="Strong Knight City",
                tier=CityTier.FORTIFIED_CITY,
                garrison=(
                    EmpireKnight(),
                    EmpireKnight(),
                    EmpireKnight(),
                    EmpireKnight(),
                ),
            ),
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
            Skeleton(),
            starting_tile=game_map.get_tile_by_cors(3, 8),
        )
    )
    game_map.create_capital_cities(WarlordAttacker, WarlordDefender)

    WarlordAttacker.add_squad(
        Squad(
            Skeleton(),
            SkeletonRider(),
            Skeleton(),
            starting_tile=game_map.get_tile_by_cors(5, 1),
        )
    )
    WarlordDefender.add_squad(
        Squad(
            EmpireKnight(),
            EmpireKnight(),
            EmpireKnight(),
            starting_tile=game_map.get_tile_by_cors(0, 1),
        )
    )

    main_game_loop(game_map, WarlordAttacker, WarlordDefender)
