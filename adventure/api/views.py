############################################################

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from adventure.models import Tile, Player, sides

############################################################


def response_data(player, messages=None, errors=None):

    if messages is None:
        messages = []

    if errors is None:
        errors = []

    tile = player.get_current_tile()

    return {
        "player": player.as_dict(),
        "tile": tile.as_dict(),
        "messages": messages,
        "errors": errors,
    }


@csrf_exempt
@api_view(["POST"])
def start(request):

    user = request.user
    player = user.player

    return Response(
        data=response_data(
            player=player,
            messages=[
                "You just started your adventure.",
            ],
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
    next_tile = None

    if requested_direction not in sides.keys():

        return Response(
            data=response_data(
                player=player,
                messages=[
                    f"You can't move in the direction \"{requested_direction}\".",
                ],
                errors=[
                    f"You can't move in the direction \"{requested_direction}\".",
                ],
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )

    else:

        side = sides[requested_direction]["to"]
        next_tile = getattr(tile, f"to_{side}")

    requested_direction_name = sides[requested_direction]["name"]

    if next_tile is not None:

        player.current_tile = next_tile
        player.save()

        return Response(
            data=response_data(
                player=player,
                messages=[
                    f"You move {requested_direction_name}.",
                ],
            ),
            status=status.HTTP_202_ACCEPTED,
        )

    else:

        return Response(
            data=response_data(
                player=player,
                messages=[
                    f"You can't move {requested_direction_name}.",
                ],
                errors=[
                    f"You can't move {requested_direction_name}.",
                ],
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
            messages=[
                "You can't speak yet.",
            ],
            errors=[
                "You can't speak yet.",
            ],
        ),
        status=status.HTTP_501_NOT_IMPLEMENTED,
    )
