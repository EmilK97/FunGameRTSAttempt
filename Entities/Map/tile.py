from Entities.Map.terrain import Terrain
import pygame
import attrs


@attrs.define
class TileCoordinates:
    x_cor: int
    y_cor: int


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_coordinates: TileCoordinates, terrain: Terrain, *groups):
        super().__init__(*groups)
        self.tile_coordinates = tile_coordinates
        self.terrain = terrain
        self.image = self.terrain.pygame_image
        self.rect = self.image.get_rect()

    @property
    def x_cor(self) -> int:
        return self.tile_coordinates.x_cor

    @property
    def y_cor(self) -> int:
        return self.tile_coordinates.y_cor

    def __str__(self):
        return f"{str(self.terrain)}: {self.x_cor}x{self.y_cor}"

    def __repr__(self):
        return self.__str__()

    def draw(self, surface: pygame.Surface, map):
        self.rect.center = map.get_tile_px_placement(self)
        surface.blit(self.image, self.rect)
