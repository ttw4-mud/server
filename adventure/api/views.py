############################################################

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from adventure.models import Tile, Player

############################################################


@csrf_exempt
@api_view(["POST"])
def start(request):

    user = request.user
    player = user.player
    tile = player.get_current_tile()

    data = {
        "player": {
            "uuid": player.uuid,
            "name": player.user.username,
        },
        "tile": {
            "name": tile.name,
            "description": tile.description,
            "players": tile.get_players_in_tile(),
        },
    }

    return Response(data=data, status=status.HTTP_202_ACCEPTED)
