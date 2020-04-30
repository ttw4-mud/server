############################################################

from rest_framework import serializers

from adventure.models import Tile, Player

############################################################


class TileSerializer(serializers.ModelSerializer):

    class Meta:

        model = Tile
        fields = [
            "id",
            "name",
            "description",
            "to_n",
            "to_s",
            "to_e",
            "to_w",
        ]


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:

        model = Player
        fields = [
            "id",
            "uuid",
            "user",
            "current_tile",
        ]
