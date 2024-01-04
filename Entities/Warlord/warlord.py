import pygame

from Engine.process_image import add_border_to_image
from Entities.Unit.squad import Squad
from Enums.colors import BLACK
from settings import SQUAD_ICON


class Warlord:
    def __init__(self, name: str, color: tuple[int] = BLACK):
        self.name = name
        self._squads = []
        self.color = color
        self._warlord_squad_icon_path = add_border_to_image(
            SQUAD_ICON, self.color, path_suffix=f"{str(self)}_squad_icon"
        )

    @property
    def squads(self) -> list[Squad]:
        return self._squads

    def add_squad(self, squad: Squad):
        squad.image = pygame.image.load(self._warlord_squad_icon_path)
        self._squads.append(squad)

    def remove_squad(self, squad: Squad):
        self._squads.remove(squad)

    def __str__(self):
        return self.name
