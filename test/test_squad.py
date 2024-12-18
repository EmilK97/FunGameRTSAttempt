import pytest

from Enums.exceptions import SquadSizeLimitReach


def test_smoke_add_trooper_to_squad(empty_squad, skeleton):
    assert len(empty_squad) == 0
    empty_squad.append(skeleton)
    assert len(empty_squad) == 1


def test_smoke_add_remove_trooper_from_squad(one_skeleton_squad, skeleton):
    test_squad = one_skeleton_squad
    assert len(test_squad) == 1
    one_skeleton_squad.append(skeleton)
    assert len(test_squad) == 2
    test_squad.remove(skeleton)
    assert len(test_squad) == 1


def test_reject_append_if_squad_size_too_bid(full_skeleton_squad, skeleton):
    with pytest.raises(SquadSizeLimitReach):
        full_skeleton_squad.append(skeleton)


def test_reject_extend_if_squad_size_too_bid(full_skeleton_squad, one_skeleton_squad):
    with pytest.raises(SquadSizeLimitReach):
        full_skeleton_squad.extend(one_skeleton_squad)


def test_squad_speed(full_skeleton_squad):
    assert full_skeleton_squad.speed == full_skeleton_squad[0].speed


def test_squad_speed_is_slowest(empty_squad, skeleton, empire_knight):
    new_squad = empty_squad
    new_squad.append(empire_knight)
    assert new_squad.speed == empire_knight.speed
    new_squad.append(skeleton)
    assert new_squad.speed == skeleton.speed
