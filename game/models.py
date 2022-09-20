from django.db import models


# Create your models here.

class Game(models.Model):
    """
    Model to Store Game Details
    """
    name = models.CharField("Game name", max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class Ship(models.Model):
    """
    Model to store Ship Details
    """
    DIRECTION = (
        ('H', 'H'),
        ('V', 'V'),
    )
    size = models.IntegerField(default=0, blank=True)
    direction = models.CharField(max_length=1, choices=DIRECTION, null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True)
    sink = models.BooleanField(default=False, blank=True)


class Coordinates(models.Model):
    """
    Model to store the cordinates of the ship location
    """
    x = models.IntegerField(default=0, blank=True)
    y = models.IntegerField(default=0, blank=True)
    hit = models.BooleanField(default=False)
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, null=True, blank=True)
