

class Map:
    def __init__(self, cities, tiles):
        self.cities = cities
        self.tiles = tiles

    def print_layout(self):
        for tile in self.tiles.values():
            pos = tile.position
            dval = tile.dice_value
            res = tile.resource

            print("pos: {}, dval: {}, res: {}" .format(pos, dval, res))
