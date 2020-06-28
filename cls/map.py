

class Map:
    def __init__(self, cities, tiles):
        self.cities = cities
        self.tiles = tiles

        self._setup()

    def print_layout(self):
        for tile in self.tiles:
            pos = tile.position
            dval = tile.dice_value
            res = tile.resource

            print("pos: {}, dval: {}, res: {}" .format(pos, dval, res))

    def __lt__(self, other, city_idx = 10):
        return self.city_probability_ranking[city_idx].probability < \
            other.city_probability_ranking[city_idx].probability

    def info(self):
        city_probs = [round(c.probability, 2) for c in self.city_probability_ranking[0:10]]
        print("city_probs: ", city_probs)

    def _setup(self):
        self.__set_resource_probabilities()
        self.__set_city_probability_ranking()


    def __set_resource_probabilities(self):
        resource_probabilities = {}

        for tile in self.tiles:
            res = tile.resource
            prob = tile.probability

            if res in resource_probabilities:
                resource_probabilities[res] += prob
            else:
                resource_probabilities[res] = prob

        del resource_probabilities["gold"]
        self.resource_probabilities = resource_probabilities

    def __set_city_probability_ranking(self):
        city_probability_ranking = sorted(self.cities, key = lambda x: x.probability, reverse = True)
        self.city_probability_ranking = city_probability_ranking
