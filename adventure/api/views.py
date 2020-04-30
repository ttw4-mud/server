############################################################

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from adventure.models import Tile, Player, sides

############################################################


def response_data(player, errors=None):

    tile = player.get_current_tile()

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

    return Response(
        data=response_data(player=player),
        status=status.HTTP_202_ACCEPTED,
    )


@csrf_exempt
@api_view(["POST"])
def move(request):

    user = request.user
    player = user.player
    tile = player.get_current_tile()

    requested_direction = request.data["direction"]
    next_tile = None

    if requested_direction not in sides.keys():

        return Response(
            data=response_data(
                player=player,
                errors=["You can't move that way."],
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )

    elif requested_direction == "n":

        next_tile = tile.to_n

    elif requested_direction == "s":

        next_tile = tile.to_s

    elif requested_direction == "e":

        next_tile = tile.to_e

    elif requested_direction == "w":

        next_tile = tile.to_w

    else:

        print("HOW DID YOU GET HERE!?")
        return Response(
            data=response_data(
                player=player,
                errors=["We done programmed this wrong."],
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if next_tile is not None:

        player.current_tile = next_tile
        player.save()

        return Response(
            data=response_data(player=player),
            status=status.HTTP_202_ACCEPTED,
        )

    else:

        return Response(
            data=response_data(
                player=player,
                errors=["You can't move that way."],
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )


@csrf_exempt
@api_view(["POST"])
def speak(request):

    user = request.user
    player = user.player

    return Response(
        data=response_data(
            player=player,
            errors=["You can't speak yet."],
        ),
        status=status.HTTP_501_NOT_IMPLEMENTED,
    )
