from typing import Optional

from Engine.combat import FieldCombatHandler, CitySiegeHandler
from Entities.City.city import City
from Entities.Map.gamemap import GameMap
from Entities.Map.tile import Tile
from Entities.Unit.squad import Squad
from Entities.Warlord.warlord import Warlord


def is_tile_overlapping_with_any_of_squads(
    tile: Tile, squads_to_check: list[Squad]
) -> Optional[Squad]:
    for squad_to_check in squads_to_check:
        if squad_to_check.tile_location == tile:
            return squad_to_check


def is_tile_overlapping_with_any_of_cities(
    tile: Tile, cities_to_check: list[City]
) -> Optional[City]:
    for city_to_check in cities_to_check:
        if city_to_check.tile_location == tile:
            return city_to_check


def handle_squad_move_attempt(
    target_tile: Tile,
    squad_to_move: Squad,
    moving_squad_warlord: Warlord,
    inactive_warlord: Warlord,
    game_map: GameMap,
):
    """Checks collision with other entities, if target tile already occupied.
    Initialize combat if target tile occupied by enemy [opposing warlord's] squad, initializes siege if tile occupied by
    enemy [opposition's warlord] city, joins garrison if target tile is friendly city.
    """
    # Check if collides with enemy squad - should initiate field combat.
    if defender_squad := is_tile_overlapping_with_any_of_squads(
        target_tile, inactive_warlord.squads
    ):
        has_squad_to_move_won = FieldCombatHandler(
            attacker_squad=squad_to_move,
            defender_squad=defender_squad,
            terrain=target_tile.terrain,
        ).execute_field_combat()
        if has_squad_to_move_won:
            inactive_warlord.remove_squad(defender_squad)
            squad_to_move.move_to_tile(target_tile)
        else:
            # If squad to move lost, remove it from list.
            moving_squad_warlord.remove_squad(squad_to_move)

    # Check if collides with player squad - should joins squad or fail if size toto big.
    elif is_tile_overlapping_with_any_of_squads(
        target_tile, moving_squad_warlord.squads
    ):
        print("ERROR - merging squads not implemented!!")

    # Check if collides with any city:
    elif colliding_city := is_tile_overlapping_with_any_of_cities(
        target_tile, game_map.cities
    ):
        # Check if collides with enemy city - should initiate siege.
        if colliding_city in inactive_warlord.cities:
            has_squad_to_move_won = CitySiegeHandler(
                attacker_squad=squad_to_move, defender_city=colliding_city
            ).execute_city_siege()
            if has_squad_to_move_won:
                # If Squad won, warlords gain city, other warlord loses city.
                # squad_to_move.move_to_tile(target_tile)
                inactive_warlord.lose_city(colliding_city)
                moving_squad_warlord.gain_city(colliding_city)
            else:
                # If squad to move lost, remove it from list.
                moving_squad_warlord.remove_squad(squad_to_move)

        # Check if collides with player City - should add to garrison.
        elif colliding_city in moving_squad_warlord.cities:
            print("ERROR - adding to garrison not implemented!!")
        # Else is a neutral city
        else:
            has_squad_to_move_won = CitySiegeHandler(
                attacker_squad=squad_to_move, defender_city=colliding_city
            ).execute_city_siege()
            if has_squad_to_move_won:
                # If Squad won, warlords gain city.
                moving_squad_warlord.gain_city(colliding_city)
            else:
                # If squad to move lost, remove it from list.
                moving_squad_warlord.remove_squad(squad_to_move)

    else:  # Tile is free, move squad
        squad_to_move.move_to_tile(target_tile)
