############################################################

############################################################

pixels = {
    "none": "·",
    "wall": "█",
    "open": " ",
}


def pixel_grid_of_no_tile():

    return [[pixels["none"] for c in range(3)] for r in range(3)]


def pixel_grid_of_walled_tile():
    return [[(pixels["wall"] if r != 1 or c != 1 else pixels["open"])
             for c in range(3)]
            for r in range(3)]


def pixel_grid_of_tile(tile):

    pixel_grid = None

    if tile is None:

        pixel_grid = pixel_grid_of_no_tile()

    else:

        pixel_grid = pixel_grid_of_walled_tile()

        if tile.has_to_side("n"):
            pixel_grid[0][1] = pixels["open"]

        if tile.has_to_side("e"):
            pixel_grid[1][2] = pixels["open"]

        if tile.has_to_side("s"):
            pixel_grid[2][1] = pixels["open"]

        if tile.has_to_side("w"):
            pixel_grid[1][0] = pixels["open"]

    return pixel_grid


def pixel_rows_of_tile(tile):

    pixel_grid = pixel_grid_of_tile(tile)
    pixel_rows = ["".join(pixel_grid_row) for pixel_grid_row in pixel_grid]

    return pixel_rows
