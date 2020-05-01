############################################################

import random

from adventure.models import sides, Tile

############################################################


def get_connected_sides(tile, row, col):
    """
    Get a list of connected sides of the tile.
    True -> connected
    False -> not connected
    """
    pass


def get_locked_sides(tile, row, col):
    """
    Get a list of locked sides of the tile. Currently connected sides are locked.
    True -> locked
    False -> not locked
    """
    pass


def generate_new_sides(tile, row, col):
    """
    Generate a list of which sides to connect. Currently locked sides cannot be connected.
    True -> to be connected
    False -> not to be connected
    """
    pass


def has_any_connected_sides(tile, row, col):
    """
    Test if a tile has _any_ connected sides.
    """
    pass
