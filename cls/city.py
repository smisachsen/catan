

class City:
    def __init__(self, position, tiles):
        self.position = position
        self.tiles = tiles
        self.name = "_".join([str(t.dice_value) for t in tiles])

        self.probability = None

        self._set_probability()

    def _set_probability(self):
        #sets the probability of obtaining a resource from the connected tiles
        prob = 0
        for tile in self.tiles:
            prob += tile.probability

        self.probability = prob

    def info(self):
        print("-"*20)
        print("city position: ", self.position)
        print("-"*20)
