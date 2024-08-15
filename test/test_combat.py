from Engine.combat import FieldCombatHandler, CitySiegeHandler


def test_squad_to_squad_field_combat_attacker_won(
    one_skeleton_squad, full_skeleton_squad, plains_terrain
):
    attacker_won = FieldCombatHandler(
        attacker_squad=full_skeleton_squad,
        defender_squad=one_skeleton_squad,
        terrain=plains_terrain,
        delay_s=0,
    ).execute_field_combat()
    assert attacker_won


def test_squad_to_squad_field_combat_attacker_lost(
    one_skeleton_squad, full_skeleton_squad, plains_terrain
):
    attacker_won = FieldCombatHandler(
        attacker_squad=one_skeleton_squad,
        defender_squad=full_skeleton_squad,
        terrain=plains_terrain,
        delay_s=0,
    ).execute_field_combat()
    assert not attacker_won


def test_city_siege_combat_attacker_won(one_skeleton_squad, city_outpost_with_garrison):
    hp_before_siege = one_skeleton_squad[0].current_hp
    attacker_won = CitySiegeHandler(
        attacker_squad=one_skeleton_squad,
        defender_city=city_outpost_with_garrison,
        delay_s=0,
    ).execute_city_siege()

    assert attacker_won

    hp_after_siege = one_skeleton_squad[0].current_hp
    # Assert attacker took one arrow.
    assert hp_before_siege > hp_after_siege


def test_city_siege_combat_attacker_lost(
    one_skeleton_squad, city_outpost_with_garrison, empire_knight
):
    city_outpost_with_garrison.add_troopers_to_garrison(empire_knight)
    attacker_won = CitySiegeHandler(
        attacker_squad=one_skeleton_squad,
        defender_city=city_outpost_with_garrison,
        delay_s=0,
    ).execute_city_siege()
    assert not attacker_won


def test_city_siege_against_empty_city(
    one_skeleton_squad, basic_city_empty_garrison, empire_knight
):
    hp_before_siege = one_skeleton_squad[0].current_hp
    attacker_won = CitySiegeHandler(
        attacker_squad=one_skeleton_squad,
        defender_city=basic_city_empty_garrison,
        delay_s=0,
    ).execute_city_siege()

    assert attacker_won

    hp_after_siege = one_skeleton_squad[0].current_hp
    # Assert attacker took one arrow.
    assert hp_before_siege == hp_after_siege
