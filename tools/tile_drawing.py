############################################################

import math

from tools.iter_tools import list_join

############################################################

PIXELS = {
    "none": "·",
    "wall": "█",
    "open": " ",
    "player": "#",
}

TILE_ROWS = 5
TILE_COLS = 5

TILE_NORTH_ROW = 0
TILE_SOUTH_ROW = TILE_ROWS - 1
TILE_WEST_COL = 0
TILE_EAST_COL = TILE_COLS - 1

TILE_SIDE_ROWS = (TILE_NORTH_ROW, TILE_SOUTH_ROW)
TILE_SIDE_COLS = (TILE_WEST_COL, TILE_EAST_COL)

TILE_CENTER_ROW = TILE_ROWS // 2
TILE_CENTER_COL = TILE_COLS // 2

############################################################


def pixel_grid_of_no_tile(show_player=False):

    pixel_grid = [[PIXELS["none"] for c in range(TILE_COLS)] for r in range(TILE_ROWS)]

    if show_player:
        pixel_grid[TILE_CENTER_ROW][TILE_CENTER_COL] = PIXELS["player"]

    return pixel_grid


def pixel_grid_of_walled_tile(show_player=False):

    pixel_grid = [[(
        PIXELS["wall"] if r in TILE_SIDE_ROWS or c in TILE_SIDE_COLS else PIXELS["open"]
    ) for c in range(TILE_COLS)] for r in range(TILE_ROWS)]

    if show_player:
        pixel_grid[TILE_CENTER_ROW][TILE_CENTER_COL] = PIXELS["player"]

    return pixel_grid


def pixel_grid_of_tile(tile, show_player=False):

    pixel_grid = None

    if tile is None:

        pixel_grid = pixel_grid_of_no_tile(show_player=show_player)

    else:

        pixel_grid = pixel_grid_of_walled_tile(show_player=show_player)

        if tile.has_to_side("n"):
            pixel_grid[TILE_NORTH_ROW][TILE_CENTER_COL] = PIXELS["open"]

        if tile.has_to_side("e"):
            pixel_grid[TILE_CENTER_ROW][TILE_EAST_COL] = PIXELS["open"]

        if tile.has_to_side("s"):
            pixel_grid[TILE_SOUTH_ROW][TILE_CENTER_COL] = PIXELS["open"]

        if tile.has_to_side("w"):
            pixel_grid[TILE_CENTER_ROW][TILE_WEST_COL] = PIXELS["open"]

    return pixel_grid


def pixel_grid_of_tile_list(tile_list):

    pixel_grid_list = [pixel_grid_of_tile(tile) for tile in tile_list]

    pixel_grid = [[]] * TILE_ROWS
    for i in range(len(pixel_grid_list)):
        for r in range(len(pixel_grid_list[i])):
            pixel_grid[r] += pixel_grid_list[i][r]

    return pixel_grid


def pixel_rows_of_tile(tile, show_player=False):

    pixel_grid = pixel_grid_of_tile(tile, show_player=show_player)
    pixel_rows = ["".join(pixel_grid_row) for pixel_grid_row in pixel_grid]

    return pixel_rows


def pixel_rows_of_tile_list(tile_list):

    pixel_rows_list = [pixel_rows_of_tile(tile) for tile in tile_list]

    pixel_rows = [""] * TILE_ROWS
    for i in range(len(pixel_rows_list)):
        for r in range(len(pixel_rows_list[i])):
            pixel_rows[r] += pixel_rows_list[i][r]

    return pixel_rows


def draw_tile(tile, show_player=False):

    return "\n".join(pixel_rows_of_tile(tile, show_player=show_player))


def draw_tile_row(tile_row):

    return "\n".join(pixel_rows_of_tile_list(tile_row))


def draw_tile_grid(tile_grid):

    return "\n".join([draw_tile_row(tile_row) for tile_row in tile_grid])
