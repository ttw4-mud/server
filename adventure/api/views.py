############################################################

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from adventure.models import Tile, Player

############################################################

directions = {
    "n": "north",
    "s": "south",
    "e": "east",
    "w": "west",
}


def response_data(player, tile, errors=None):

    return {
        "player": player.as_dict(),
        "tile": {
            "name": tile.name,
            "description": tile.description,
            "players": tile.get_players_in_tile(),
        },
        "errors": errors,
    }


@csrf_exempt
@api_view(["POST"])
def start(request):

    user = request.user
    player = user.player
    tile = player.get_current_tile()

    return Response(
        data=response_data(
            player=player,
            tile=tile,
        ),
        status=status.HTTP_202_ACCEPTED,
    )


@csrf_exempt
@api_view(["POST"])
def move(request):

    user = request.user
    player = user.player
    tile = player.get_current_tile()

    requested_direction = request.data["direction"]
    next_tile_id = None

    if requested_direction not in directions.keys():

        return Response(
            data=response_data(
                player=player,
                tile=tile,
                errors=["You cannot move that way."],
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )

    elif requested_direction == "n":

        next_tile_id = tile.to_n

    elif requested_direction == "s":

        next_tile_id = tile.to_s

    elif requested_direction == "e":

        next_tile_id = tile.to_e

    elif requested_direction == "w":

        next_tile_id = tile.to_w

    else:

        print("HOW DID YOU GET HERE!?")
        return Response(
            data=response_data(
                player=player,
                tile=tile,
                errors=["We done programmed this wrong."],
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if next_tile_id is not None:

        next_tile = Tile.objects.get(id=next_tile_id)

        player.current_tile = next_tile_id
        player.save()

        return Response(
            data=response_data(
                player=player,
                tile=next_tile,
            ),
            status=status.HTTP_202_ACCEPTED,
        )

    else:

        return Response(
            data=response_data(
                player=player,
                tile=tile,
                errors=["You cannot move that way."],
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )


@csrf_exempt
@api_view(["POST"])
def speak(request):

    user = request.user
    player = user.player
    tile = player.get_current_tile()

    return Response(
        data=response_data(
            player=player,
            tile=tile,
            errors=["You can't do that yet."],
        ),
        status=status.HTTP_501_NOT_IMPLEMENTED,
    )
