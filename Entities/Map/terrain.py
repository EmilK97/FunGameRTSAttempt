from abc import ABC
from Enums.landscape import Landscape
import attrs


@attrs.define
class Terrain(ABC):
    landscape: Landscape
    movement_cost: int
    texture_path: str

    def __str__(self):
        return self.landscape.name


class Plains(Terrain):
    def __init__(self):
        super().__init__(Landscape.PLAINS, 2, "path")


class Forest(Terrain):
    def __init__(self):
        super().__init__(Landscape.FOREST, 3, "path")
