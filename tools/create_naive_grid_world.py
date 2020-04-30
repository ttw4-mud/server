############################################################

from adventure.models import Player, Tile
from tools.tile_drawing import (
    pixel_rows_of_tile,
    pixel_rows_of_tile_list,
)

############################################################


def print_tile(tile):

    print("\n".join(pixel_rows_of_tile(tile)))


def print_tile_row(tile_row):

    print("\n".join(pixel_rows_of_tile_list(tile_row)))


def create_naive_grid_world(n_rows, n_cols):

    # DEFINE TILES
    tile_grid = [[Tile() for c in range(n_cols)] for r in range(n_rows)]

    # PRINT TILES
    print()

    for r in range(len(tile_grid)):
        print_tile_row(tile_grid[r])

    print()

    # START ALL PLAYERS

    players = Player.objects.all()

    for p in players:

        p.current_tile = tile_grid[0][0]
        p.save()

    #

    return
