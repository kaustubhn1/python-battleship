from django.contrib import admin
from .models import Game, Ship, Coordinates

# Register your models here.
admin.site.register(Game)
admin.site.register(Ship)
admin.site.register(Coordinates)