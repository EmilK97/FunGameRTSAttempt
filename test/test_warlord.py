def test_warlord_add_squad(one_skeleton_squad, basic_warlord):
    basic_warlord.add_squad(one_skeleton_squad)


def test_warlord_remove_squad(one_skeleton_squad, basic_warlord):
    basic_warlord.add_squad(one_skeleton_squad)
    basic_warlord.remove_squad(one_skeleton_squad)


def test_warlord_gain_city(basic_city_empty_garrison, basic_warlord):
    assert len(basic_warlord.cities) == 0
    basic_warlord.gain_city(basic_city_empty_garrison)
    assert len(basic_warlord.cities) == 1


def test_warlord_lose_city(basic_city_empty_garrison, basic_warlord):
    basic_warlord.gain_city(basic_city_empty_garrison)
    assert len(basic_warlord.cities) == 1
    basic_warlord.lose_city(basic_city_empty_garrison)
    assert len(basic_warlord.cities) == 0
