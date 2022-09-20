# Django imports
from django.shortcuts import render
from .models import Game, Coordinates, Ship

# Rest framework imports
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .base_helpers import create_ships


class GameViews(ViewSet):
    """
    Class to implement APIs for battleship game
    """

    def __init__(self, **kwargs):
        """Initializer class"""
        super(GameViews, self).__init__(**kwargs)

    def create_a_game(self, request):
        """Method to create or update existing game

        Args:
            request (POST): POST Request
        """
        try:
            game = Game.objects.all().first() or Game.objects.create(name="Battleship")
            ships = request.data.get('ships')
            for ship in ships:
                status, message = create_ships(game, ship)
                if not status:
                    return Response({"error": message}, status=400)
            return Response({"message": "Ok"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def play_game(self, request):
        """
        Method to play the game

        Args:
            request (PUT): PUT Request
        """
        try:
            x = int(request.data.get('x'))
            y = int(request.data.get('y'))
            if not 0 <= x <= 9 or not 0 <= y <= 9:
                return Response({"error": "Hit going overboard"}, status=400)
            if not Coordinates.objects.filter(x=x, y=y).exists():
                return Response({"result": "WATER"}, status=200)

            coords = Coordinates.objects.filter(x=x, y=y).first()

            if coords.ship.sink:
                return Response({"result": "HIT"}, status=200)
            if not coords.hit:
                coords.hit = True
                coords.save()
            ship_coords = Coordinates.objects.filter(ship=coords.ship)
            if False in [ship.hit for ship in ship_coords]:
                return Response({"result": "HIT"}, status=200)
            coords.ship.sink = True
            coords.ship.save()
            return Response({"result": "SINK"}, status=200)
        except Exception as e:
            return Response({"status": 500, "error": str(e)})

    def delete_game(self, request):
        """
        Method to delete the game

        Args:
            request (DELETE): Delete Request

        Returns:
            Deletes the Game object from database
        """
        Game.objects.all().delete()
        return Response({"result": "Deleted the Game"})
