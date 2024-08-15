import pytest

from Entities.City.city import City
from Entities.Map.NeutralCityTemplate import NeutralCityTemplate
from Entities.Map.gamemap import GameMap
from Entities.Map.terrain import PLAINS, Terrain
from Entities.Map.tile import TileCoordinates, Tile
from Entities.Unit.empire_trooper import EmpireKnight
from Entities.Unit.squad import Squad
from Entities.Unit.undead_trooper import Skeleton
from Entities.Warlord.warlord import Warlord
from Enums.city_tier import CityTier
from Enums.factions import Factions
from Enums.races import Races


@pytest.fixture
def basic_game_map() -> GameMap:
    """With two neutral cities."""
    return GameMap(
        x_length=9,
        y_length=16,
        for_amount_of_players=2,
        players_starting_coordinates_in_order=(
            TileCoordinates(3, 3),
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


@pytest.fixture
def zero_cors_tile(basic_game_map: GameMap) -> Tile:
    basic_game_map.get_tile_by_cors(0, 0)


@pytest.fixture
def basic_warlord():
    return Warlord(
        "TestWarlord",
        capital_city_name="TestCapital",
        favorite_faction=Factions.EMPIRE,
        favorite_race=Races.ELF,
    )


@pytest.fixture
def skeleton():
    return Skeleton()


@pytest.fixture
def empire_knight():
    return EmpireKnight()


@pytest.fixture
def empty_squad(zero_cors_tile):
    return Squad(starting_tile=zero_cors_tile)


@pytest.fixture
def one_skeleton_squad(zero_cors_tile):
    return Squad(Skeleton(), starting_tile=zero_cors_tile)


@pytest.fixture
def full_skeleton_squad(zero_cors_tile):
    return Squad(
        Skeleton(),
        Skeleton(),
        Skeleton(),
        Skeleton(),
        Skeleton(),
        Skeleton(),
        Skeleton(),
        Skeleton(),
        starting_tile=zero_cors_tile,
    )


@pytest.fixture
def basic_city_empty_garrison(zero_cors_tile) -> City:
    return City(
        race=Races.ELF,
        faction=Factions.EMPIRE,
        name="BasicCity",
        tile_location=zero_cors_tile,
        tier=CityTier.CITY,
    )


@pytest.fixture
def city_outpost_with_garrison(zero_cors_tile, one_skeleton_squad) -> City:
    """Weak city with single man garrison."""
    city = City(
        race=Races.ELF,
        faction=Factions.EMPIRE,
        name="BasicCity",
        tile_location=zero_cors_tile,
        tier=CityTier.OUTPOST,
    )
    city.add_troopers_to_garrison(one_skeleton_squad[0])
    return city


@pytest.fixture
def plains_terrain(zero_cors_tile) -> Terrain:
    return PLAINS
