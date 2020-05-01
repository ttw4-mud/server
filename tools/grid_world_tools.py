############################################################

import random

from adventure.models import sides, Tile

############################################################


def get_connected_sides(tile, row=None, col=None, grid_size=(None, None)):
    """
    Get a list of connected sides of the tile.
    True -> connected
    False -> not connected
    """

    return [tile.has_to_side(side) for side in sides.keys()]


def has_any_connected_sides(tile, row=None, col=None, grid_size=(None, None)):
    """
    Test if a tile has _any_ connected sides.
    """

    return any(get_connected_sides(tile, row, col, grid_size))


def get_locked_sides(tile, row, col, grid_size):
    """
    Get a list of locked sides of the tile. Currently connected sides are locked.
    True -> locked
    False -> not locked
    """


def generate_new_sides(tile, row, col, grid_size):
    """
    Generate a list of which sides to connect. Currently locked sides cannot be connected.
    True -> to be connected
    False -> not to be connected
    """
    pass
