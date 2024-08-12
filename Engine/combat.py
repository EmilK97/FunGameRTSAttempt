import logging
from time import sleep

from Entities.Unit.squad import Squad
from Entities.Unit.trooper import Trooper
from Entities.Warlord.warlord import Warlord
from Enums.exceptions import CombatUnitListEmpty


class CombatHandler:
    attacker_squad: Squad
    defender_squad: Squad

    def __init__(
        self,
        attacker_squad: Squad,
        attacker_warlord: Warlord,
        defender_squad: Squad,
        defender_warlord: Warlord,
        delay_s: int = 0.2,
    ):
        self.delay_s = delay_s
        self.attacker_squad = attacker_squad
        self.attacker_warlord = attacker_warlord
        self.defender_squad = defender_squad
        self.defender_warlord = defender_warlord

    def execute_field_combat(self) -> True:
        """Executes field combat turn sequence. Returns True if attacker has won else False."""
        self._start_combat()
        while True:
            try:
                attacker, defender = self.pick_combatants()
                self._execute_combat_round(attacker, defender)
            except CombatUnitListEmpty:
                if not self.attacker_squad:
                    self.attacker_warlord.remove_squad(self.attacker_squad)
                    return self._end_combat(losing_warlord=self.attacker_warlord)
                else:
                    self.defender_warlord.remove_squad(self.defender_squad)
                    return self._end_combat(losing_warlord=self.defender_warlord)

    def _start_combat(self):
        pass

    def _end_combat(self, losing_warlord: Warlord) -> bool:
        """Returns True if attacker has won else false."""
        logging.info("Combat finished!")
        logging.info(f"{str(losing_warlord)} lost!!!")
        logging.info(f"DEFENDER {[str(unit) for unit in self.defender_squad]}")
        logging.info(f"ATTACKER {[str(unit) for unit in self.attacker_squad]}")
        return losing_warlord == self.attacker_warlord

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
