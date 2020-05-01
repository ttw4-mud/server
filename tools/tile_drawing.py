############################################################

from tools.iter_tools import list_join

############################################################

pixels = {
    "none": "·",
    "wall": "█",
    "open": " ",
    "player": "#",
}


def pixel_grid_of_no_tile(show_player=False):

    pixel_grid = [[pixels["none"] for c in range(3)] for r in range(3)]

    if show_player:
        pixel_grid[1][1] = pixels["player"]

    return pixel_grid


def pixel_grid_of_walled_tile(show_player=False):

    pixel_grid = [[(pixels["wall"] if r != 1 or c != 1 else pixels["open"])
                   for c in range(3)]
                  for r in range(3)]

    if show_player:
        pixel_grid[1][1] = pixels["player"]

    return pixel_grid


def pixel_grid_of_tile(tile, show_player=False):

    pixel_grid = None

    if tile is None:

        pixel_grid = pixel_grid_of_no_tile(show_player=show_player)

    else:

        pixel_grid = pixel_grid_of_walled_tile(show_player=show_player)

        if tile.has_to_side("n"):
            pixel_grid[0][1] = pixels["open"]

        if tile.has_to_side("e"):
            pixel_grid[1][2] = pixels["open"]

        if tile.has_to_side("s"):
            pixel_grid[2][1] = pixels["open"]

        if tile.has_to_side("w"):
            pixel_grid[1][0] = pixels["open"]

    return pixel_grid


def pixel_grid_of_tile_list(tile_list):

    pixel_grid_list = [pixel_grid_of_tile(tile) for tile in tile_list]

    pixel_grid = [[]] * 3
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

    pixel_rows = [""] * 3
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
