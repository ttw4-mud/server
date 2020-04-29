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
        "player": {
            "uuid": player.uuid,
            "name": player.user.username,
        },
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
        pass
    elif requested_direction == "s":
        pass
    elif requested_direction == "e":
        pass
    elif requested_direction == "w":
        pass
    else:
        print("HOW DID YOU GET HERE!?")

    return Response(
        data=response_data(
            player=player,
            tile=tile,
        ),
        status=status.HTTP_202_ACCEPTED,
    )
