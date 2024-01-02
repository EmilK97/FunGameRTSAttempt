from Entities.Map.tile import Tile
from Entities.Map.terrain import Plains, Forest


class Map:
    def __init__(self, x_length, y_length, name="TestMap"):
        self.x_length = x_length
        self.y_length = y_length
        self.name = name
        self._tiles = list()
        for x in range(self.x_length):
            for y in range(self.y_length):
                if y < 7:
                    self._tiles.append(Tile(x, y, Plains()))
                else:
                    self._tiles.append(Tile(x, y, Forest()))

        self._tiles = tuple(self._tiles)

    def get_tile_by_cors(self, x_cor: int, y_cor: int) -> Tile:
        def has_cors(x, y, tile):
            return tile.x_cor == x and tile.y_cor == y

        return next((tile for tile in self.__iter__() if has_cors(x_cor, y_cor, tile)))

    def __iter__(self):
        return iter(self._tiles)

    def __next__(self):
        return next(self.__iter__())

    def __str__(self):
        return f"{self.name}: {self.x_length}x{self.y_length}"

    def find_route_to_tile(self, start_tile: Tile, target_tile: Tile):
        pass
