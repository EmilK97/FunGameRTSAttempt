import logging
from time import sleep
from typing import Optional

from Entities.City.city import City
from Entities.Map.terrain import Terrain
from Entities.Unit.squad import Squad
from Entities.Unit.trooper import Trooper
from Enums.exceptions import CombatUnitListEmpty


class CombatHandler:
    attacker_squad: Squad
    defender_squad: Squad

    def __init__(
        self,
        attacker_squad: Squad,
        defender_squad: Squad,
        terrain: Terrain,
        defender_city: Optional[City] = None,
        delay_s: int = 0.2,
    ):
        self.delay_s = delay_s
        self.attacker_squad = attacker_squad
        self.defender_squad = defender_squad
        self.defender_city = defender_city
        self.terrain = terrain

    def execute_field_combat(self) -> True:
        """Executes field combat turn sequence. Returns True if attacker has won else False."""
        self._start_combat()
        while True:
            try:
                attacker, defender = self.pick_combatants()
                self._execute_combat_round(attacker, defender)
            except CombatUnitListEmpty:
                return self._end_combat()

    def _start_combat(self):
        logging.info(
            f"Combat initiated between squads: attacker {self.attacker_squad.id}, defender: {self.defender_squad.id}."
        )
        if self.defender_city is not None:
            logging.info(f"Combat in City: {self.defender_city}")
        else:
            logging.info(f"Combat started in terrain: {self.terrain}")

    def _end_combat(self) -> bool:
        """Returns True if attacker has won else false."""
        attacker_won = bool(self.attacker_squad)
        logging.info(f"Attacker won: {attacker_won}!")
        logging.info("Combat finished.")
        logging.info(f"DEFENDER {[str(unit) for unit in self.defender_squad]}")
        logging.info(f"ATTACKER {[str(unit) for unit in self.attacker_squad]}")
        return attacker_won

    def pick_combatants(self) -> tuple[Trooper, Trooper]:
        if not self.attacker_squad or not self.defender_squad:
            raise CombatUnitListEmpty
        return self.attacker_squad[0], self.defender_squad[0]

    def _execute_attack(self, damager: Trooper, damagee: Trooper):
        damagee.current_hp = damagee.current_hp - damager.strength
        logging.debug(f"\n{str(damager)}\nATTACKED\n{str(damagee)}\n\n")
        sleep(self.delay_s)

    def _execute_combat_round(self, attacking_unit: Trooper, defending_unit: Trooper):
        while True:
            # Attacker attack
            self._execute_attack(attacking_unit, defending_unit)
            if defending_unit.is_dead:
                self.defender_squad.remove(defending_unit)
                return
                # Defender attack
            self._execute_attack(defending_unit, attacking_unit)
            if attacking_unit.is_dead:
                self.attacker_squad.remove(attacking_unit)
                return
