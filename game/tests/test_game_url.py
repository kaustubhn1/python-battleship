# Django imports
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from game.views import GameViews


class GameURLsTestCases(SimpleTestCase):
    """
    API Test Cases to test Game APIs
    """

    def test_create_game_api(self):
        url = reverse('battleship-game')
        self.assertEqual(resolve(url).func.cls, GameViews)
