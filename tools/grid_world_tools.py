############################################################

import random

from adventure.models import sides

############################################################


def translate_side_bools_to_side_keys(side_bools):
    """
    Translate list of True/False sides to keys of True sides.
    """

    return [
        sides.keys()[i] for (i, side_bool) in enumerate(side_bools) if side_bool is True
    ]


#-----------------------------------------------------------


def get_connected_side_bools(tile, row=None, col=None, grid_size=(None, None)):
    """
    Get a list of connected sides of the tile.
    True -> connected
    False -> not connected
    """

    return [tile.has_to_side(side) for side in sides.keys()]


def get_connected_sides(tile, row=None, col=None, grid_size=(None, None)):
    """
    Get a list of connected sides of the tile.
    """

    return translate_side_bools_to_side_keys(
        get_connected_side_bools(tile, row, col, grid_size)
    )


def has_any_connected_sides(tile, row=None, col=None, grid_size=(None, None)):
    """
    Test if a tile has _any_ connected sides.
    """

    return any(get_connected_side_bools(tile, row, col, grid_size))


#-----------------------------------------------------------


def get_locked_side_bools(tile, row, col, grid_size):
    """
    Get a list of locked sides of the tile. Currently connected sides are locked.
    True -> locked
    False -> not locked
    """

    # currently connected sides are necessarily locked
    locked_sides = get_connected_side_bools(tile, row, col, grid_size)

    # if tile in first row, can't go north
    if row <= 0:
        locked_sides[sides.index("n")] = True

        # if tile in last row, can't go south
    if row >= (grid_size[0] - 1):
        locked_sides[sides.index("s")] = True

    # if tile in first col, can't go west
    if col <= 0:
        locked_sides[sides.index("w")] = True

    # if tile in last col, can't go east
    if col >= (grid_size[1] - 1):
        locked_sides[sides.index("e")] = True

    return locked_sides


def get_locked_sides(tile, row, col, grid_size):
    """
    Get a list of locked sides of the tile. Currently connected sides are locked.
    """

    return translate_side_bools_to_side_keys(
        get_locked_side_bools(tile, row, col, grid_size)
    )


#-----------------------------------------------------------


def generate_new_side_bools(tile, row, col, grid_size):
    """
    Generate a list of which sides to newly connect.
    May generate no new connections.
    Currently locked sides cannot be connected.
    True -> to be connected
    False -> not to be connected
    """

    locked_sides = get_locked_side_bools(tile, row, col, grid_size)

    # if side is locked (True): no new side (False)
    # else: generate random True or False
    new_sides = [(False if side is True else random.choice((True, False)))
                 for side in locked_sides]

    return new_sides


def generate_new_sides(tile, row, col, grid_size):
    """
    Generate a list of which sides to newly connect.
    May generate no new connections.
    Currently locked sides cannot be connected.
    """

    return translate_side_bools_to_side_keys(
        generate_new_side_bools(tile, row, col, grid_size)
    )


#-----------------------------------------------------------


def always_generate_new_side_bools(tile, row, col, grid_size, min_new_sides=1):
    """
    Generate a list of which sides to newly connect.
    Always generates new sides (`min_new_sides`, default 1)
    ... _unless_ too few unlocked sides are available.
    Currently locked sides cannot be connected.
    True -> to be connected
    False -> not to be connected
    """

    count_all_sides = len(sides.keys())
    count_locked_sides = sum(get_locked_side_bools(tile, row, col, grid_size))
    max_new_sides = count_all_sides - count_locked_sides

    # adjust min_new_sides if there are too few unlocked sides available
    min_new_sides = min_new_sides if min_new_sides < max_new_sides else max_new_sides

    # keep trying until min_new_sides is satisfied
    new_sides = None
    count_new_sides = None

    while count_new_sides is None or count_new_sides < min_new_sides:
        # try to generate enough new sides
        new_sides = generate_new_side_bools(tile, row, col, grid_size)
        # we can't count the already locked sides as "new"
        count_new_sides = sum(new_sides) - count_locked_sides

    # at this point, min_new_sides should be satisifed
    return new_sides


def always_generate_new_sides(tile, row, col, grid_size, min_new_sides=1):
    """
    Generate a list of which sides to newly connect.
    Always generates new sides (`min_new_sides`, default 1)
    ... _unless_ too few unlocked sides are available.
    Currently locked sides cannot be connected.
    """

    return translate_side_bools_to_side_keys(
        always_generate_new_side_bools(tile, row, col, grid_size)
    )
