from Entities.Unit.squad import Squad


class Warlord:
    def __init__(self, name: str):
        self.name = name
        self._squads = []

    @property
    def squads(self) -> list[Squad]:
        return self._squads

    def add_squad(self, squad: Squad):
        self._squads.append(squad)

    def remove_squad(self, squad: Squad):
        self._squads.remove(squad)

    def __str__(self):
        return self.name
