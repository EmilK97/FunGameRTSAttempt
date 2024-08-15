import logging
from abc import ABC
from time import sleep

from Entities.City.city import City
from Entities.Map.terrain import Terrain
from Entities.Unit.squad import Squad, Garrison
from Entities.Unit.trooper import Trooper
from Enums.exceptions import CombatUnitListEmpty


class AbstractCombatHandler(ABC):
    def __init__(
        self,
        attacker_squad: Squad,
        delay_s: int = 0.2,
    ):
        self.delay_s = delay_s
        self.attacker_squad = attacker_squad

    def pick_combatants(
        self, defender_squad: Squad | Garrison
    ) -> tuple[Trooper, Trooper]:
        if not self.attacker_squad or not defender_squad:
            raise CombatUnitListEmpty
        return self.attacker_squad[0], defender_squad[0]

    def _execute_trooper_attack(self, damager: Trooper, damagee: Trooper):
        damagee.take_damage(damager.strength)
        logging.debug(f"\n{str(damager)}\nATTACKED\n{str(damagee)}\n\n")
        sleep(self.delay_s)


class FieldCombatHandler(AbstractCombatHandler):
    def __init__(
        self,
        attacker_squad: Squad,
        defender_squad: Squad,
        terrain: Terrain,
        delay_s: int = 0.2,
    ):
        super().__init__(attacker_squad, delay_s)
        self.defender_squad = defender_squad
        self.terrain = terrain

    def _start_combat(self):
        logging.info(
            f"Combat initiated between squads: attacker {self.attacker_squad.id}, defender: {self.defender_squad.id}."
        )

        logging.info(f"Combat started in terrain: {self.terrain}")

    def _end_combat(self) -> bool:
        """Returns True if attacker has won else false."""
        attacker_won = bool(self.attacker_squad)
        logging.info(f"Attacker won: {attacker_won}!")
        logging.info("Combat finished.")
        logging.info(f"DEFENDER {[str(unit) for unit in self.defender_squad]}")
        logging.info(f"ATTACKER {[str(unit) for unit in self.attacker_squad]}")
        return attacker_won

    def execute_field_combat(self) -> True:
        """Executes field combat turn sequence. Returns True if attacker has won else False."""
        self._start_combat()
        while True:
            try:
                attacker, defender = self.pick_combatants(self.defender_squad)
                self._execute_field_combat_round(attacker, defender)
            except CombatUnitListEmpty:
                return self._end_combat()

    def _execute_field_combat_round(
        self, attacking_unit: Trooper, defending_unit: Trooper
    ):
        """Executes combat round encounter between two troopers."""
        while True:
            # Attacker attack
            self._execute_trooper_attack(attacking_unit, defending_unit)
            if defending_unit.is_dead:
                self.defender_squad.remove(defending_unit)
                return
                # Defender attack
            self._execute_trooper_attack(defending_unit, attacking_unit)
            if attacking_unit.is_dead:
                self.attacker_squad.remove(attacking_unit)
                return


class CitySiegeHandler(AbstractCombatHandler):
    def __init__(self, attacker_squad: Squad, defender_city: City, delay_s: int = 0.2):
        super().__init__(attacker_squad, delay_s)
        self.defender_city = defender_city
        self.defender_garrison: Garrison = defender_city.garrison

    def execute_city_siege(self):
        """Executes city siege combat turn sequence. Returns True if attacker has won else False."""
        if not self.defender_city.is_garrison_populated:
            # If garrison empty, end combat automatically.
            logging.debug(
                "Combat lost automatically because defender city had empty garrison."
            )
            self._end_combat()

        self._start_combat()
        while True:
            try:
                attacker, defender = self.pick_combatants(self.defender_garrison)
                self._execute_city_siege_combat_round(attacker, defender)
            except CombatUnitListEmpty:
                return self._end_combat()

    def _start_combat(self):
        logging.info(
            f"Combat initiated between squads: attacker {self.attacker_squad.id}, garrison: {self.defender_garrison.id}."
        )
        logging.info(f"Combat in City: {self.defender_city}")

    def _end_combat(self) -> bool:
        """Returns True if attacker has won else false."""
        attacker_won = bool(self.attacker_squad)
        logging.info(f"Attacker won: {attacker_won}!")
        logging.info("Combat finished.")
        logging.info(f"DEFENDER {[str(unit) for unit in self.defender_garrison]}")
        logging.info(f"ATTACKER {[str(unit) for unit in self.attacker_squad]}")
        return attacker_won

    def _fire_arrow_at_attacker(self, attacker_tooper: Trooper):
        attacker_tooper.take_damage(self.defender_city.combat_strength)
        logging.debug(
            f"\n{str(self.defender_city)}\nFIRED ARROW AT\n{str(attacker_tooper)}\n\n"
        )
        sleep(self.delay_s)

    def _execute_city_siege_combat_round(
        self, attacking_unit: Trooper, defending_unit: Trooper
    ):
        """Executes combat round encounter between two troopers from attacker squad and defender garrison.
        Fires an arrow at attacker before encounter begins."""
        self._fire_arrow_at_attacker(attacking_unit)
        if attacking_unit.is_dead:
            self.attacker_squad.remove(attacking_unit)
            return

        while True:
            # Attacker attack
            self._execute_trooper_attack(attacking_unit, defending_unit)
            if defending_unit.is_dead:
                self.defender_garrison.remove(defending_unit)
                return
                # Defender attack
            self._execute_trooper_attack(defending_unit, attacking_unit)
            if attacking_unit.is_dead:
                self.attacker_squad.remove(attacking_unit)
                return
