import pytest

from Engine.main_game_loop import main_game_loop
from Entities.Map.tile import Tile
from Enums.exceptions import WrongNumberOfWarlordsForMap


def test_smoke_run_map(basic_game_map, basic_warlord):
    main_game_loop(
        basic_game_map, basic_warlord, basic_warlord, kill_after_one_loop=True
    )


def test_create_capital_cities(basic_game_map, basic_warlord):
    basic_game_map.create_capital_cities(basic_warlord, basic_warlord)


def test_map_has_only_two_neutral_cities(basic_game_map):
    assert len(basic_game_map.cities) == 2
    assert len(basic_game_map.capital_cities) == 0


def test_map_add_neutral_city(basic_game_map, basic_warlord):
    assert len(basic_game_map.cities) == 2
    basic_game_map.create_capital_cities(basic_warlord, basic_warlord)
    assert len(basic_game_map.cities) == 4
    assert [c_city in basic_game_map.cities for c_city in basic_game_map.capital_cities]


def test_too_few_warlords_for_create_capital_cities(basic_game_map, basic_warlord):
    with pytest.raises(WrongNumberOfWarlordsForMap):
        basic_game_map.create_capital_cities(basic_warlord)


def test_too_many_warlords_for_create_capital_cities(basic_game_map, basic_warlord):
    with pytest.raises(WrongNumberOfWarlordsForMap):
        basic_game_map.create_capital_cities(
            basic_warlord, basic_warlord, basic_warlord
        )


def test_game_loop_too_many_warlords(basic_game_map, basic_warlord):
    with pytest.raises(TypeError):
        main_game_loop(
            basic_game_map,
            basic_warlord,
            basic_warlord,
            basic_warlord,
            kill_after_one_loop=True,
        )


def test_map_click_out_of_range(basic_game_map):
    """Click px way out of range of basic map, expect None returned."""
    clicked_tile = basic_game_map.get_tile_by_px_click(
        basic_game_map.MAP_BORDER / 2, basic_game_map.MAP_BORDER / 2
    )
    assert clicked_tile is None


def test_map_click_on_tile(basic_game_map):
    """Click px in range of basic map, expect returned tile in maps tiles."""
    clicked_tile = basic_game_map.get_tile_by_px_click(
        basic_game_map.MAP_BORDER, basic_game_map.MAP_BORDER
    )
    assert isinstance(clicked_tile, Tile)
    assert any([clicked_tile == tile for tile in basic_game_map])
