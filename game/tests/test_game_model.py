from django.test import TestCase
from game.models import Game, Coordinates, Ship


class TestGameModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.game = Game.objects.create(name="Battleship")

    def test_game_name_type_string(self):
        self.assertEqual(self.game.name, "Battleship")


class TestShipModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.game = Game.objects.create(name="Battleship")
        cls.size = 4
        cls.direction = "H"
        cls.sink = False
        cls.ship = Ship.objects.create(game=cls.game, size=cls.size, direction=cls.direction)

    def test_ship_game_object(self):
        self.assertEqual(self.ship.game, self.game)

    def test_ship_direction(self):
        self.assertEqual(self.ship.direction, self.direction)

    def test_ship_size(self):
        self.assertEqual(self.ship.size, self.size)

    def test_ship_direction_as_string(self):
        self.assertEqual(type(self.ship.direction), str)

    def test_ship_size_as_integer(self):
        self.assertEqual(type(self.ship.size), int)


class TestCoordinatesModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.game = Game.objects.create(name="Battleship")
        cls.size = 4
        cls.direction = "H"
        cls.sink = False
        cls.ship = Ship.objects.create(game=cls.game, size=cls.size, direction=cls.direction)
        cls.coordinates = Coordinates.objects.create(ship=cls.ship, x=2, y=3)

    def test_coordinates_x_type_int(self):
        self.assertEqual(type(self.coordinates.x), int)

    def test_coordinates_y_type_int(self):
        self.assertEqual(type(self.coordinates.y), int)
