from pygame import Rect, Surface, font

from settings import BUTTON_FONT_SIZE, BUTTON_WIDTH, BUTTON_HEIGHT


class Button:
    name: str
    rect: Rect
    button_text: Surface

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        button_color,
        hover_color,
        text: str,
        text_color,
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        font_size=BUTTON_FONT_SIZE,
        font_name=None,
    ):
        self.name = name
        self.rect = Rect(x, y, width, height)  # x, y, width, height
        self.button_text = font.Font(font_name, font_size).render(
            text, True, text_color
        )
        self.button_color = button_color
        self.hover_color = hover_color

    def __str__(self):
        return f"{self.name} button."
