from django.urls import path
from .views import GameViews

urlpatterns = [
    path('', GameViews.as_view({
        'post': "create_a_game",
        "delete": "delete_game",
        'put': "play_game"}), name="battleship-game"),
]
