from .models import Coordinates, Ship


def create_ships(game, ship):
    """Create a new ship"""
    try:
        if int(ship['size']) < 1:
            return False, "Ship size must atleast be 1"
        if int(ship['x']) < 0 or int(ship['y']) < 0:
            return False, "Coordinates cannot be negative"
        for coords in Coordinates.objects.all():
            if coords.x == int(ship['x']) and coords.y == int(ship['y']):
                return False, "Ships are overlapping"

        if ship['direction'] == "V":
            if int(ship['y']) + int(ship['size']) > 9:
                return False, "Ship is going overboard"
        elif int(ship['x']) + int(ship['size']) > 9:
            return False, "Ship is going overboard"

        ship_object = Ship.objects.create(game=game, direction=ship['direction'], size=int(ship['size']))

        if ship['direction'] == "V":
            for y_cord in range(int(ship['size'])):
                Coordinates.objects.create(ship=ship_object, x=int(ship['x']), y=int(ship['y']) + y_cord)
        else:
            for x_cord in range(int(ship['size'])):
                Coordinates.objects.create(ship=ship_object, x=int(ship['x']) + x_cord, y=int(ship['y']))
        return True, None
    except Exception as e:
        return False, str(e)
