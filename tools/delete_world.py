############################################################

from adventure.models import Tile

############################################################


def delete_world():

    Tile.objects.all().delete()

    return
