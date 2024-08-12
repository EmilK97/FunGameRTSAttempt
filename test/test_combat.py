from copy import deepcopy

from Engine.combat import CombatHandler


def test_smoke_squad_to_squad_combat_attacker_won(
    one_skeleton_squad, full_skeleton_squad, basic_warlord
):
    attacker_warlord = basic_warlord
    defender_warlord = deepcopy(basic_warlord)
    attacker_warlord.add_squad(full_skeleton_squad)
    defender_warlord.add_squad(one_skeleton_squad)

    attacker_won = CombatHandler(
        attacker_squad=full_skeleton_squad,
        attacker_warlord=attacker_warlord,
        defender_squad=one_skeleton_squad,
        defender_warlord=defender_warlord,
        delay_s=0,
    ).execute_field_combat()
    assert attacker_won
