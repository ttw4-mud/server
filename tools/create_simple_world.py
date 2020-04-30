############################################################

from adventure.models import Player, Tile

############################################################


def create_simple_world():

    # DEFINE TILES

    tile_outside = Tile(
        name="Outside Cave Entrance",
        description="""North of you, the cave mount beckons.""",
    )

    tile_foyer = Tile(
        name="Foyer",
        description="""Dim light filters in from the south. Dusty
    passages run north and east."""
    )

    tile_overlook = Tile(
        name="Grand Overlook",
        description="""A steep cliff appears before you, falling
    into the darkness. Ahead to the north, a light flickers in
    the distance, but there is no way across the chasm."""
    )

    tile_narrow = Tile(
        name="Narrow Passage",
        description="""The narrow passage bends here from west
    to north. The smell of gold permeates the air."""
    )

    tile_treasure = Tile(
        name="Treasure Chamber",
        description="""You've found the long-lost treasure
    chamber! Sadly, it has already been completely emptied by
    earlier adventurers. The only exit is to the south."""
    )

    tile_outside.save()
    tile_foyer.save()
    tile_overlook.save()
    tile_narrow.save()
    tile_treasure.save()

    # CONNECT TILES

    tile_outside.connect_to("n", tile_foyer)
    tile_foyer.connect_to("s", tile_outside)

    tile_foyer.connect_to("n", tile_overlook)
    tile_overlook.connect_to("s", tile_foyer)

    tile_foyer.connect_to("e", tile_narrow)
    tile_narrow.connect_to("w", tile_foyer)

    tile_narrow.connect_to("n", tile_treasure)
    tile_treasure.connect_to("s", tile_narrow)

    # START ALL PLAYERS

    players = Player.objects.all()

    for p in players:

        p.current_tile = tile_outside
        p.save()

    #

    return
