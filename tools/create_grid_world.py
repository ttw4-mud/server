############################################################

from adventure.models import Tile, Player
from tools.grid_world_tools import always_generate_new_sides, get_offsets_for_to_side
from tools.tile_drawing import draw_tile_grid

############################################################

DEFAULT_N_ROWS = 8
DEFAULT_N_COLS = 8
DEFAULT_NEW_SIDE_ODDS = (1, 2)
DEFAULT_MIN_NEW_SIDES = 1

############################################################


def create_grid_world(
    n_rows=DEFAULT_N_ROWS,
    n_cols=DEFAULT_N_COLS,
    new_side_odds=DEFAULT_NEW_SIDE_ODDS,
    min_new_sides=DEFAULT_MIN_NEW_SIDES,
):

    # DEFINE TILES

    tile_grid = [[Tile() for c in range(n_cols)] for r in range(n_rows)]

    # SAVE ALL TILES

    for row in range(n_rows):
        for col in range(n_cols):
            tile_grid[row][col].save()

    # CONNECTION TILES

    for row in range(n_rows):

        for col in range(n_cols):

            from_tile = tile_grid[row][col]

            # randomly choose to connect to adjacent tiles
            new_sides = always_generate_new_sides(
                from_tile,
                row,
                col,
                (n_rows, n_cols),
                min_new_sides=min_new_sides,
            )

            # need to connect BOTH ways
            for new_side in new_sides:

                # select tile to connect to
                (row_offset, col_offset) = get_offsets_for_to_side(new_side)
                to_tile = tile_grid[row + row_offset][col + col_offset]

                # connect them
                Tile.connect_from_to(new_side, from_tile, to_tile)

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
