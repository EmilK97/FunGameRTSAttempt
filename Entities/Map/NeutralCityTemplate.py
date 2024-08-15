import attrs

from Entities.Map.tile import TileCoordinates
from Entities.Unit.trooper import Trooper
from Enums.city_tier import CityTier
from Enums.factions import Factions
from Enums.races import Races


@attrs.define
class NeutralCityTemplate:
    tile_coordinates: TileCoordinates
    garrison: tuple[Trooper, ...]
    name: str
    faction: Factions
    race: Races
    tier: CityTier
