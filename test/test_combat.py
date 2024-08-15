from copy import deepcopy

from Engine.combat import CombatHandler


def test_smoke_squad_to_squad_combat_attacker_won(
    one_skeleton_squad, full_skeleton_squad, plains_terrain
):
    attacker_won = CombatHandler(
        attacker_squad=full_skeleton_squad,
        defender_squad=one_skeleton_squad,
        terrain=plains_terrain,
        delay_s=0,
    ).execute_field_combat()
    assert attacker_won


def test_smoke_squad_to_squad_combat_attacker_lost(
    one_skeleton_squad, full_skeleton_squad, plains_terrain
):
    attacker_won = CombatHandler(
        attacker_squad=one_skeleton_squad,
        defender_squad=full_skeleton_squad,
        terrain=plains_terrain,
        delay_s=0,
    ).execute_field_combat()
    assert not attacker_won
