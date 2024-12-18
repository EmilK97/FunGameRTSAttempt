from typing import Optional

from Entities.City.city import CapitalCity, City
from Entities.Map.NeutralCityTemplate import NeutralCityTemplate
from Entities.Map.terrain import PLAINS, FOREST, MOUNTAIN
from Entities.Map.tile import Tile, TileCoordinates
from Entities.Warlord.warlord import Warlord
from Enums.exceptions import TileOutOfMapRange, WrongNumberOfWarlordsForMap
from settings import TILE_IMAGE_SIZE_PX


class GameMap:
    MAP_BORDER = 80

    def __init__(
            self,
            *,
            x_length,
            y_length,
            name="TestMap",
            for_amount_of_players: int = 2,
            players_starting_coordinates_in_order: tuple[..., TileCoordinates],
            neutral_cities_template: tuple[NeutralCityTemplate, ...],
    ):
        self.for_amount_of_players = for_amount_of_players
        self.x_length = x_length
        self.y_length = y_length
        self.name = name
        self._tiles = list()
        if len(players_starting_coordinates_in_order) != self.for_amount_of_players:
            raise RuntimeError(
                f"Starting players location amount not equal to amount of players for which map is intended"
            )
        self.players_starting_location: tuple[
            ..., TileCoordinates
        ] = players_starting_coordinates_in_order

        self.cities: list[City] = []
        self.capital_cities: list[CapitalCity] = []

        for x in range(self.x_length):
            mountain_coordinates = ((7, 2), (8, 3), (9, 4), (5, 3), (4, 3))
            forest_coordinates = (
            (7, 3), (8, 4), (9, 5), (2, 3), (2, 2), (1, 1), (1, 2), (3, 3), (5, 3), (4, 4), (5, 4))
            for y in range(self.y_length):
                if (x, y) in mountain_coordinates:
                    self._tiles.append(Tile(TileCoordinates(x, y), MOUNTAIN))
                elif (x, y) in forest_coordinates:
                    self._tiles.append(Tile(TileCoordinates(x, y), FOREST))
                elif x > 12:
                    self._tiles.append(Tile(TileCoordinates(x, y), FOREST))
                elif y > 7 or y < 1:
                    self._tiles.append(Tile(TileCoordinates(x, y), MOUNTAIN))
                else:
                    self._tiles.append(Tile(TileCoordinates(x, y), PLAINS))

        self._tiles = tuple(self._tiles)
        self.create_neutral_cities(neutral_cities_template)

    def create_capital_cities(self, *warlords: Warlord):
        if len(warlords) != self.for_amount_of_players:
            raise WrongNumberOfWarlordsForMap

        for warlord, starting_location in zip(warlords, self.players_starting_location):
            warlord_capital_city = CapitalCity(
                race=warlord.favorite_race,
                faction=warlord.favorite_faction,
                name=warlord.capital_city_name,
                tile_location=self.get_tile_by_cors(
                    starting_location.x_cor, starting_location.y_cor
                ),
            )
            self.capital_cities.append(warlord_capital_city)
            warlord.gain_city(warlord_capital_city)

        self.cities += self.capital_cities

    def create_neutral_cities(
            self,
            neutral_cities_template: tuple[NeutralCityTemplate, ...],
    ):
        for i, template in enumerate(neutral_cities_template):
            new_city = City(
                race=template.race,
                faction=template.faction,
                name=template.name,
                tile_location=self.get_tile_by_cors(
                    template.tile_coordinates.x_cor, template.tile_coordinates.y_cor
                ),
                tier=template.tier,
            )
            new_city.add_troopers_to_garrison(*template.garrison)
            self.cities.append(new_city)

    def get_tile_by_cors(self, x_cor: int, y_cor: int) -> Optional[Tile]:
        def has_cors(x, y, tile):
            return tile.x_cor == x and tile.y_cor == y

        return next(
            (tile for tile in self.__iter__() if has_cors(x_cor, y_cor, tile)), None
        )

    def get_tile_px_placement(self, tile: Tile) -> tuple[int, int]:
        try:
            found_tile = next(
                (map_tile for map_tile in self.__iter__() if map_tile == tile)
            )

            return self.MAP_BORDER + (
                    found_tile.x_cor * TILE_IMAGE_SIZE_PX
            ), self.MAP_BORDER + (found_tile.y_cor * TILE_IMAGE_SIZE_PX)
        except StopIteration:
            raise TileOutOfMapRange

    def get_tile_by_px_click(self, click_x: int, click_y: int) -> Optional[Tile]:
        clicked_x_cor = round((click_x - self.MAP_BORDER) / TILE_IMAGE_SIZE_PX)
        clicked_y_cor = round((click_y - self.MAP_BORDER) / TILE_IMAGE_SIZE_PX)

        return self.get_tile_by_cors(clicked_x_cor, clicked_y_cor)

    def __iter__(self):
        return iter(self._tiles)

    def __next__(self):
        return next(self.__iter__())

    def __str__(self):
        return f"{self.name}: {self.x_length}x{self.y_length}"
