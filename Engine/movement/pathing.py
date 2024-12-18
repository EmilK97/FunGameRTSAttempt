from typing import Optional

from Entities.Map.gamemap import GameMap
from Entities.Map.tile import Tile


def get_total_movement_cost_for_tiles(tiles: tuple[Tile, ...]) -> int:
    """Returns total cost needed to be spent to move through tile list."""
    return sum([tile.terrain.movement_cost for tile in tiles])


def find_last_path_index_speed_allows_to_reach(
    speed: int, path: tuple[Tile, ...]
) -> Optional[int]:
    """Returns tile index from given path which given speed can reach. None means not enough movement to move."""
    max_tile_range_index = None
    if len(path) == 1 and speed >= get_total_movement_cost_for_tiles(path):
        max_tile_range_index = 0

    for i in range(1, len(path)):
        path_movement_cost = get_total_movement_cost_for_tiles(path[:-i])
        if speed > path_movement_cost:
            max_tile_range_index = len(path) - i
            break
    return max_tile_range_index


def find_movement_path(
    starting_tile: Tile, target_tile: Tile, game_map: GameMap
) -> tuple[Tile, ...]:
    """Returns set of tile in order and total movement cost.
    Assumptions: can't move sideways (only East/ North/ Sout / West squares)."""
    current_placement_cor_x = starting_tile.tile_coordinates.x_cor
    current_placement_cor_y = starting_tile.tile_coordinates.y_cor
    tile_path_order = []

    x_cor_diff = target_tile.tile_coordinates.x_cor - current_placement_cor_x
    y_cor_diff = target_tile.tile_coordinates.y_cor - current_placement_cor_y

    while True:
        X_AXIS_MOVEMENT_DIRECTION = (
            "LEFT" if x_cor_diff < 0 else "RIGHT" if x_cor_diff > 0 else "EQUAL"
        )
        Y_AXIS_MOVEMENT_DIRECTION = (
            "UP" if y_cor_diff < 0 else "DOWN" if y_cor_diff > 0 else "EQUAL"
        )

        if (
            X_AXIS_MOVEMENT_DIRECTION == "EQUAL"
            and Y_AXIS_MOVEMENT_DIRECTION == "EQUAL"
        ):
            break

        # Get cost of movement on next tile for X axis
        if X_AXIS_MOVEMENT_DIRECTION == "EQUAL":
            x_tile_candidate = None
        elif X_AXIS_MOVEMENT_DIRECTION == "LEFT":
            x_tile_candidate = game_map.get_tile_by_cors(
                x_cor=current_placement_cor_x - 1, y_cor=current_placement_cor_y
            )
        else:
            x_tile_candidate = game_map.get_tile_by_cors(
                x_cor=current_placement_cor_x + 1, y_cor=current_placement_cor_y
            )
        # Get cost of movement on next tile for Y axis
        if Y_AXIS_MOVEMENT_DIRECTION == "EQUAL":
            y_tile_candidate = None
        elif Y_AXIS_MOVEMENT_DIRECTION == "UP":
            y_tile_candidate = game_map.get_tile_by_cors(
                x_cor=current_placement_cor_x, y_cor=current_placement_cor_y - 1
            )
        else:
            y_tile_candidate = game_map.get_tile_by_cors(
                x_cor=current_placement_cor_x, y_cor=current_placement_cor_y + 1
            )

        if y_tile_candidate is None:
            tile_to_move = x_tile_candidate
        elif x_tile_candidate is None:
            tile_to_move = y_tile_candidate
        else:
            y_tile_candidate_cost = y_tile_candidate.terrain.movement_cost
            x_tile_candidate_cost = x_tile_candidate.terrain.movement_cost

            # IF y tile cost is greater than X, use X tile candidate, else use Y tile candidate
            if y_tile_candidate_cost > x_tile_candidate_cost:
                tile_to_move = x_tile_candidate
            else:
                tile_to_move = y_tile_candidate

        tile_path_order.append(tile_to_move)
        current_placement_cor_x = tile_to_move.x_cor
        current_placement_cor_y = tile_to_move.y_cor
        x_cor_diff = target_tile.tile_coordinates.x_cor - current_placement_cor_x
        y_cor_diff = target_tile.tile_coordinates.y_cor - current_placement_cor_y

    tile_path_order = tuple(tile_path_order)
    return tile_path_order
