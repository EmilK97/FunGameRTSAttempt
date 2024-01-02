import attrs
from Entities.Map.terrain import Terrain


@attrs.define
class Tile:
    # dataclass
    x_cor: int
    y_cor: int
    terrain: Terrain

    def __str__(self):
        return f"{str(self.terrain)}: {self.x_cor}x{self.y_cor}"
