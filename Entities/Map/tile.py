from Entities.Map.terrain import Terrain
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, x_cor: int, y_cor: int, terrain: Terrain, *groups):
        super().__init__(*groups)
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.terrain = terrain
        self.image = self.terrain.pygame_image
        self.rect = self.image.get_rect()

    def draw(self, surface: pygame.Surface, map):
        self.rect.center = map.get_tile_px_placement(self)
        surface.blit(self.image, self.rect)

    def __str__(self):
        return f"{str(self.terrain)}: {self.x_cor}x{self.y_cor}"
