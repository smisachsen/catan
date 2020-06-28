import json
import random

from collections import Counter

class Island:
    def __init__(self, name, initial_tile):
        self.name = name
        self.initial_tile = initial_tile
        self.tiles = []

        self.add_tile(initial_tile)

    def __lt__(self, other):
        return len(self) < len(other)


    def __repr__(self):
        return self.name

    def __len__(self):
        return len(self.tiles)

    def add_tile(self, tile, output = False):
        assert tile not in self.tiles
        self.tiles.append(tile)
        tile.island = self

        if output:
            print(f"added {tile} to {self}")

    def info(self):
        print("-"*20)
        print(self)
        for tile in self.tiles:
            print(tile)
        print("-"*20)

    def can_add_tile(self):
        neighbouring_tiles = set(neighbour for tile in self.tiles
            for neighbour in tile.get_neighbours()
            if neighbour != None and not neighbour.touches_another_island(self)
            and not neighbour in self.tiles
            )

        return len(neighbouring_tiles) > 0


    def get_candidate_tile(self):
        """
        returns random tile object that can be added to island without touching
        another island
        """

        neighbouring_tiles = set(neighbour for tile in self.tiles
            for neighbour in tile.get_neighbours()
            if neighbour != None and not neighbour.touches_another_island(self)
            and not neighbour in self.tiles
            )

        return random.choice(list(neighbouring_tiles))


class Tile:
    def __init__(self, position):
        self.position = position
        self.island = None

        #neigbouring tiles
        self.north = None
        self.north_east = None
        self.south_east = None
        self.south = None
        self.south_west = None
        self.north_west = None

    def touches_another_island(self, island):
        neighbours = self.get_neighbours()
        return any(neighbour.island != None and neighbour.island != island
            for neighbour in neighbours if neighbour != None)

    def get_neighbours(self):
        return [self.north,
            self.north_east,
            self.south_east,
            self.south,
            self.south_west,
            self.north_west]

    def set_south_east_neighbour(self, tile):
        self.south_east = tile
        tile.north_west = self

    def set_north_neighbour(self, tile):
        self.north = tile
        tile.south = self

    def set_south_west_neighbour(self, tile):
        self.south_west = tile
        tile.north_east = self

    def print_neighbours(self):
        print("-"*20)
        print(self)
        print("north:", self.north)
        print("south:" ,self.south)
        print("south_east:", self.south_east)
        print("south_west:", self.south_west)
        print("north_east:", self.north_east)
        print("north_west:", self.north_west)

    def __repr__(self):
        return "tile" + str(self.position)



def get_tiles_list_with_neighbours():
    """
    returns a list of Tile objects with links to neighbours, edges have value: None
    """
    num_tiles = 44
    tiles = {pos: Tile(pos) for pos in range(1, num_tiles+1)}

    #add all south_east/north_west pairs
    exclude = [4, 9, 15, 22, 29, 35, 40, 44] #edges of board
    neighbours = {i: dict() for i in range(1,num_tiles+1)}

    for i in range(1, num_tiles+1):
        if i not in exclude:
            tiles[i].set_south_east_neighbour(tiles[i+1])


    #add south/north pairs along right side of board
    tiles[9].set_north_neighbour(tiles[4])
    tiles[15].set_north_neighbour(tiles[9])
    tiles[22].set_north_neighbour(tiles[15])
    tiles[29].set_north_neighbour(tiles[22])

    #add south_east/north_west along bottom right side of board
    tiles[29].set_south_west_neighbour(tiles[35])
    tiles[35].set_south_west_neighbour(tiles[40])
    tiles[40].set_south_west_neighbour(tiles[44])
    tiles[39].set_south_west_neighbour(tiles[43])
    tiles[38].set_south_west_neighbour(tiles[42])
    tiles[37].set_south_west_neighbour(tiles[41])
    tiles[1].set_south_west_neighbour(tiles[5])
    tiles[5].set_south_west_neighbour(tiles[10])
    tiles[10].set_south_west_neighbour(tiles[16])

    #use recursion to find other neighbour pairs from south/north
    #south_east/north_west pairs (the south tile of a north_west neighbour will
    #be a south_west tile for the tile we are considering)

    #start from tile29 (down right) and flood the map from this tile
    top_tiles = [1, 2, 3, 4, 5, 10, 16]

    #north/south for all tiles
    south_tiles = [35, 40, 44, 43, 42, 41]

    for i in south_tiles:
        tmp_tile = tiles[i]

        while tmp_tile.position not in top_tiles:
            north = tmp_tile.north_east.north_west
            tmp_tile.set_north_neighbour(north)

            if tmp_tile.north.position not in top_tiles:
                #add north_east node (seen from north)
                tmp_tile.north_east.north.set_south_west_neighbour(north)

            tmp_tile = tmp_tile.north

    return tiles


def create_island(num_islands, resource_json = "map_generation/info/resources.json"):
    with open(resource_json, "r") as file:
        data = json.load(file)

    num_resource_tiles = sum([int(val) for val in data.values()])

    #hardcoded centers for islands (depending on num_islands)
    centers = {
        2: [16, 29],
        3: [16, 9, 42],
        4: [41, 16, 4, 29],
        5: [35, 42, 23, 1, 9],
        6: [26, 29, 41, 16, 1, 9],
        7: [10, 3, 15, 35, 42, 30, 26]
    }

    tiles = get_tiles_list_with_neighbours()
    initial_tiles = centers[num_islands]

    islands = list()
    for island_index, tile_index in enumerate(initial_tiles):
        islands.append(Island(f"Island{island_index+1}", tiles[tile_index]))

    num_tiles_left = num_resource_tiles-num_islands

    while num_tiles_left > 0:
        islands_to_select = sorted([i for i in islands if i.can_add_tile()]) #always choose the smalles island to grow
        island_to_grow = islands_to_select[0]

        tile = island_to_grow.get_candidate_tile()
        island_to_grow.add_tile(tile)

        num_tiles_left -= 1

    return islands


def write_island_to_json(num_islands, json_name):

    #some maps may lock themselves where no new tiles can be added :(
    found = False
    while not found:
        try:
            islands = create_island(num_islands)
            found = True
        except:
            pass



    map = dict()
    for island in islands:
        for tile in island.tiles:
            map[tile.position] = "random"

    #add gold tiles
    gold_indecies = random.choices(list(map.keys()), k = 2)
    for i in gold_indecies:
        map[i] = "gold"

    for i in range(1, 45):
        if not i in map.keys():
            map[i] = "water"

    resources = Counter(map.values())
    import pdb;
    assert resources["gold"] == 2, pdb.set_trace()
    assert resources["random"] == 25





    with open(json_name, "w") as file:
        json.dump(map, file, sort_keys = True)
