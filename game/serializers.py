from rest_framework.serializers import ModelSerializer
from .models import Game, Ship, Coordinates

class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"
        
class ShipSerializer(ModelSerializer):
    class Meta:
        model = Ship
        fields = "__all__"
        
class CoordinatesSerializer(ModelSerializer):
    class Meta:
        model = Coordinates
        fields = "__all__"