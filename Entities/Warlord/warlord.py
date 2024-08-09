import pygame

from Engine.process_image import add_border_to_image
from Entities.City.city import City, CapitalCity
from Entities.Map.tile import Tile
from Entities.Unit.squad import Squad
from Enums.colors import BLACK
from Enums.factions import Factions
from Enums.races import Races
from settings import SQUAD_ICON, CITY_ICON


class Warlord:
    def __init__(
        self,
        name: str,
        capital_city_name: str,
        favorite_race: Races,
        favorite_faction: Factions,
        starting_tile: Tile,
        color: tuple[int] = BLACK,
    ):
        self.name: str = name
        self._squads: list[Squad] = []
        self._cities: list[City] = []
        self.capital_city_name = capital_city_name
        self.starting_tile = starting_tile
        self.favorite_race = favorite_race
        self.favorite_faction = favorite_faction
        self.color = color
        self._warlord_squad_icon_path = add_border_to_image(
            SQUAD_ICON, self.color, path_suffix=f"{str(self)}_squad_icon"
        )
        self._warlord_city_icon_path = add_border_to_image(
            CITY_ICON, self.color, path_suffix=f"{str(self)}_city_icon"
        )

        self.create_capital_city()

    @property
    def squads(self) -> list[Squad]:
        return self._squads

    def add_squad(self, squad: Squad):
        squad.image = pygame.image.load(self._warlord_squad_icon_path)
        self._squads.append(squad)

    def remove_squad(self, squad: Squad):
        self._squads.remove(squad)

    @property
    def cities(self) -> list[City]:
        return self._cities

    def gain_city(self, city: City):
        city.image = pygame.image.load(self._warlord_city_icon_path)
        self._cities.append(city)

    def lose_city(self, city: City):
        self._cities.remove(city)

    def create_capital_city(self):
        self.gain_city(
            CapitalCity(
                race=self.favorite_race,
                faction=self.favorite_faction,
                tile_location=self.starting_tile,
                name=self.capital_city_name,
            )
        )

    def __str__(self):
        return self.name
