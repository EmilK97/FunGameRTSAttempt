from Entities.City.city import City
from Entities.Unit.squad import Squad
from Enums.colors import BLACK
from Enums.factions import Factions
from Enums.races import Races


class Warlord:
    def __init__(
        self,
        name: str,
        capital_city_name: str,
        favorite_race: Races,
        favorite_faction: Factions,
        color: tuple[int] = BLACK,
    ):
        self.name: str = name
        self._squads: list[Squad] = []
        self._cities: list[City] = []
        self.capital_city_name = capital_city_name
        self.favorite_race = favorite_race
        self.favorite_faction = favorite_faction
        self.color: tuple[int] = color

    @property
    def squads(self) -> list[Squad]:
        return self._squads

    def add_squad(self, squad: Squad):
        self._squads.append(squad)

    def remove_squad(self, squad: Squad):
        self._squads.remove(squad)

    @property
    def cities(self) -> list[City]:
        return self._cities

    def gain_city(self, city: City):
        self._cities.append(city)

    def lose_city(self, city: City):
        self._cities.remove(city)

    def __str__(self):
        return self.name
