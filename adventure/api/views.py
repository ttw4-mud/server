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
        "tile": tile.as_dict(),
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

    else:

        side = sides[requested_direction]["to"]
        next_tile = getattr(tile, f"to_{side}")

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
