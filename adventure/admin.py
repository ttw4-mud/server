############################################################

from django.contrib import admin

from adventure.models import Tile, Player

############################################################

admin.site.register(Tile)
admin.site.register(Player)
