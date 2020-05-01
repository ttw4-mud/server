############################################################

from collections import OrderedDict as odict
from uuid import uuid4

from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from tools.tile_drawing import pixel_grid_of_tile, pixel_rows_of_tile

############################################################

sides = odict({
    "n": {
        "name": "north",
        "to": "n",
        "from": "s",
    },
    "e": {
        "name": "east",
        "to": "e",
        "from": "w",
    },
    "s": {
        "name": "south",
        "to": "s",
        "from": "n",
    },
    "w": {
        "name": "west",
        "to": "w",
        "from": "e",
    },
})

corners = odict({
    "nw": "north-west",
    "ne": "north-east",
    "se": "south-east",
    "sw": "south-west",
})

############################################################


class Tile(models.Model):

    name = models.CharField(
        max_length=50,
        default="DEFAULT NAME",
        verbose_name="tile's name",
    )
    description = models.CharField(
        max_length=500,
        default="DEFAULT DESCRIPTION",
        verbose_name="tile's description",
    )
    to_n = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="tile to the north",
        related_name="tile_to_n",
    )
    to_s = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="tile to the south",
        related_name="tile_to_s",
    )
    to_e = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="tile to the east",
        related_name="tile_to_e",
    )
    to_w = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="tile to the west",
        related_name="tile_to_w",
    )

    def __str__(self):

        return f"{self.name} [{self.id}]"

    def has_to_side(self, side):

        return (getattr(self, f"to_{side}") is not None)

    def as_dict(self):

        tile_dict = {
            "name": self.name,
            "description": self.description,
        }

        for side in sides.keys():
            tile_dict[f"to_{side}"] = self.has_to_side(side)

        tile_dict["pixel_grid"] = pixel_grid_of_tile(self)
        tile_dict["pixel_rows"] = pixel_rows_of_tile(self)

        tile_dict["players"] = self.get_players_in_tile()

        return tile_dict

    def connect_to(self, to_side, to_tile):
        """
        Connect this tile to another tile in the "to" direction.
        """

        if to_side not in sides.keys():

            raise Exception("connect_to.InvalidSide")

        else:

            side = sides[to_side]["to"]
            setattr(self, f"to_{side}", to_tile)

        self.save()
        return

    def connect_from(self, from_side, from_tile):
        """
        Connect this tile from another tile in the "from" direction.
        """

        if from_side not in sides.keys():

            raise Exception("connect_from.InvalidSide")

        else:

            side = sides[from_side]["from"]
            setattr(self, f"to_{side}", from_tile)

        self.save()
        return

    @staticmethod
    def connect_from_to(direction, from_tile, to_tile):
        """
        Connect from one tile to another tile in the given direction.
        """

        from_tile.connect_to(direction, to_tile)
        to_tile.connect_from(direction, from_tile)

        return

    def get_players_in_tile(self):

        return [p.as_dict() for p in Player.objects.filter(current_tile=self.id)]

    def get_other_players_in_tile(self, current_player_id):

        return [
            p.as_dict()
            for p in Player.objects.filter(current_tile=self.id)
            if p.id != int(current_player_id)
        ]


class Player(models.Model):

    uuid = models.UUIDField(
        default=uuid4,
        unique=True,
        verbose_name="player's uuid",
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="player's user",
    )
    current_tile = models.ForeignKey(
        Tile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="player's current tile",
    )

    def __str__(self):

        return f"{self.user.username} [{self.id}]"

    def as_dict(self):

        player_dict = {
            "uuid": self.uuid,
            "name": self.user.username,
        }

        return player_dict

    def start_adventure(self):

        if self.current_tile is None:

            self.current_tile = Tile.objects.first()
            self.save()

        return

    def get_current_tile(self):

        try:

            return Tile.objects.get(id=self.current_tile.id)

        except (Tile.DoesNotExist, AttributeError):

            self.start_adventure()

            return self.get_current_tile()


@receiver(signals.post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):

    if created:

        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

    return


@receiver(signals.post_save, sender=User)
def save_user_player(sender, instance, **kwargs):

    instance.player.save()

    return
