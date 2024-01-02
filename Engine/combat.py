from Entities.Unit.trooper import Trooper
from time import sleep
from Enums.exceptions import CombatUnitListEmpty
from Entities.Unit.squad import Squad
import logging


class CombatHandler:
    attacker_units: Squad
    defender_units: Squad

    def __init__(self, attacker_units: Squad, defender_units: Squad):
        self.attacker_units = attacker_units
        self.defender_units = defender_units

    def execute_combat(self) -> tuple[Squad, Squad]:
        self._start_combat()
        while True:
            if self.defender_units and self.attacker_units:
                attacker, defender = self.pick_combatants()
                self._execute_combat_round(attacker, defender)
            else:
                self._end_combat()
                return self.attacker_units, self.defender_units

    def _start_combat(self):
        pass

    def _end_combat(self):
        logging.info("Combat finished!")
        logging.info(f"DEFENDER {[str(unit) for unit in self.defender_units]}")
        logging.info(f"ATTACKER {[str(unit) for unit in self.attacker_units]}")

    def pick_combatants(self) -> tuple[Trooper, Trooper]:
        if not self.attacker_units or not self.defender_units:
            raise CombatUnitListEmpty
        return self.attacker_units[0], self.defender_units[0]

    @staticmethod
    def _execute_attack(damager: Trooper, damagee: Trooper):
        damagee.current_hp = damagee.current_hp - damager.strength
        logging.debug(f"\n{str(damager)}\nATTACKED\n{str(damagee)}\n\n")
        sleep(0.5)

    def _execute_combat_round(self, attacking_unit: Trooper, defending_unit: Trooper):
        while True:
            # Attacker attack
            self._execute_attack(attacking_unit, defending_unit)
            if defending_unit.is_dead:
                self.defender_units.remove(defending_unit)
                return
                # Defender attack
            self._execute_attack(defending_unit, attacking_unit)
            if attacking_unit.is_dead:
                self.attacker_units.remove(attacking_unit)
                return
