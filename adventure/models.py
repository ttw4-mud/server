############################################################

from uuid import uuid4

from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

############################################################

sides = {
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
}

corners = {
    "nw": "north-west",
    "ne": "north-east",
    "se": "south-east",
    "sw": "south-west",
}

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

    def connect_to(self, to_side, to_tile):

        if to_side not in sides.keys():

            raise Exception("connect_to.InvalidSide")

        else:

            side = sides[to_side]["to"]
            setattr(self, f"to_{side}", to_tile)

        self.save()

    def connect_from(self, from_side, from_tile):

        if from_side not in sides.keys():

            raise Exception("connect_from.InvalidSide")

        else:

            side = sides[from_side]["from"]
            setattr(self, f"to_{side}", from_tile)

        self.save()

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

        return {
            "uuid": self.uuid,
            "name": self.user.username,
        }

    def start_adventure(self):

        if self.current_tile is None:

            self.current_tile = Tile.objects.first()
            self.save()

        return

    def get_current_tile(self):

        try:

            return Tile.objects.get(id=self.current_tile.id)

        except Tile.DoesNotExist:

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
