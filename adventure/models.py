############################################################

from uuid import uuid4

from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

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
    to_n = models.ManyToManyField(
        "self",
        verbose_name="tile to the north",
    )
    to_s = models.ManyToManyField(
        "self",
        verbose_name="tile to the south",
    )
    to_e = models.ManyToManyField(
        "self",
        verbose_name="tile to the east",
    )
    to_w = models.ManyToManyField(
        "self",
        verbose_name="tile to the west",
    )

    def connect_to(self, direction, destination_tile):

        destination_tile_id = destination_tile.id
        # this might raise an exception -- we want that to happen
        destination_tile = Tile.objects.get(id=destination_tile_id)

        if direction == "n":

            self.to_n = destination_tile_id

        elif direction == "s":

            self.to_s = destination_tile_id

        elif direction == "e":

            self.to_e = destination_tile_id

        elif direction == "w":

            self.to_w = destination_tile_id

        else:

            raise Exception("connect_to.InvalidDirection")

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
        verbose_name="player's current tile",
    )

    def as_dict(self):

        return {
            "uuid": self.uuid,
            "name": self.user.username,
        }

    def start_adventure(self):

        if self.current_tile == 0:

            self.current_tile = Tile.objects.first().id
            self.save()

    def get_current_tile(self):

        try:

            return Tile.objects.get(id=self.current_tile)

        except Tile.DoesNotExist:

            self.start()

            return self.tile()


@receiver(signals.post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):

    if created:

        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(signals.post_save, sender=User)
def save_user_player(sender, instance, **kwargs):

    instance.player.save()
