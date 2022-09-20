from django.urls import reverse
import json
# Rest framework imports
from rest_framework.test import APITestCase
from game.models import Game, Ship, Coordinates


class GameAPITestCases(APITestCase):

    def setUp(self):
        self.game = Game.objects.create(name="Battleship")
        self.size = 4
        self.direction = "H"
        self.sink = False
        self.ship = Ship.objects.create(game=self.game, size=self.size, direction=self.direction)
        self.coordinates = Coordinates.objects.create(ship=self.ship, x=2, y=3)
        Coordinates.objects.create(ship=self.ship, x=3, y=3)
        Coordinates.objects.create(ship=self.ship, x=4, y=3)
        Coordinates.objects.create(ship=self.ship, x=5, y=3)
        self.sinked_ship = Ship.objects.create(game=self.game, size=1, direction="V", sink=True)
        Coordinates.objects.create(ship=self.sinked_ship, x=1, y=1)

    def test_create_a_game(self):
        data = {
            "ships": [
                {
                    "x": 2,
                    "y": 1,
                    "size": 4,
                    "direction": "H"
                },
                {
                    "x": 7,
                    "y": 4,
                    "size": 3,
                    "direction": "V"
                },
                {
                    "x": 3,
                    "y": 5,
                    "size": 2,
                    "direction": "V"
                },
                {
                    "x": 6,
                    "y": 8,
                    "size": 1,
                    "direction": "H"
                }
            ]
        }
        response = self.client.post(reverse('battleship-game'), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_two_ships_cannot_overlap(self):
        data = {
            "ships": [
                {
                    "x": 2,
                    "y": 1,
                    "size": 4,
                    "direction": "H"
                },
                {
                    "x": 7,
                    "y": 4,
                    "size": 3,
                    "direction": "V"
                },
                {
                    "x": 5,
                    "y": 1,
                    "size": 2,
                    "direction": "V"
                },
                {
                    "x": 6,
                    "y": 8,
                    "size": 1,
                    "direction": "H"
                }
            ]
        }
        response = self.client.post(reverse('battleship-game'), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_if_ship_is_going_overboard(self):
        data = {
            "ships": [
                {
                    "x": 7,
                    "y": 4,
                    "size": 1,
                    "direction": "V"
                },
                {
                    "x": 5,
                    "y": 1,
                    "size": 2,
                    "direction": "V"
                },
                {
                    "x": 1,
                    "y": 9,
                    "size": 3,
                    "direction": "V"
                }
            ]
        }
        response = self.client.post(reverse('battleship-game'), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_if_ship_coordinates_are_negative(self):
        data = {
            "ships": [
                {
                    "x": -1,
                    "y": 2,
                    "size": 1,
                    "direction": "V"
                }
            ]
        }
        response = self.client.post(reverse('battleship-game'), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_if_ship_coordinates_are_greater_than_board_size(self):
        data = {
            "ships": [
                {
                    "x": 1,
                    "y": 10,
                    "size": 1,
                    "direction": "V"
                }
            ]
        }
        response = self.client.post(reverse('battleship-game'), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_if_shot_returns_water(self):
        data = {
            "x": 5,
            "y": 4
        }
        response = self.client.put(reverse('battleship-game'), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_if_shot_hits_ship(self):
        data = {
            "x": 4,
            "y": 3
        }
        response = self.client.put(reverse('battleship-game'), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_if_shot_sinks_ship(self):
        coords = Coordinates.objects.filter(ship=self.ship)
        for coord in coords:
            coord.hit = True
            coord.save()
        data = {
            "x": 4,
            "y": 3
        }
        response = self.client.put(reverse('battleship-game'), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_if_shot_hits_already_sinked_ship(self):
        data = {
            "x": 1,
            "y": 1
        }
        response = self.client.put(reverse('battleship-game'), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
