############################################################

from adventure.models import sides, Tile, Player
from tools.tile_drawing import draw_tile_grid

############################################################


def create_naive_grid_world(n_rows, n_cols):

    # DEFINE TILES

    tile_grid = [[Tile() for c in range(n_cols)] for r in range(n_rows)]

    # CONNECTION TILES

    for r in range(n_rows):

        for c in range(n_cols):

            # randomly choose to connect to adjacent tiles
            # need to connect BOTH ways
            # if tile in first row, can't go north
            # if tile in first col, can't go west
            # if tile in last row, can't go south
            # if tile in last col, can't go east
            # each tile must have at least 1 connection
            pass

    # PRINT TILES

    print()
    print(draw_tile_grid(tile_grid))
    print()

    # START ALL PLAYERS

    players = Player.objects.all()

    for p in players:

        p.current_tile = tile_grid[0][0]
        p.save()

    #

    return
