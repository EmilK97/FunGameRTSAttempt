import attrs


@attrs.define
class RgbColor:
    R: int
    G: int
    B: int

    @property
    def rgb_tuple(self) -> tuple:
        return self.R, self.G, self.B


COLORS: dict[str, RgbColor] = {
    "blue": RgbColor(0, 0, 255),
    "green": RgbColor(0, 255, 0),
}
