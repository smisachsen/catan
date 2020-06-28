import random
import json

from cls.city import City
from cls.tile import Tile
from cls.map import Map



def get_random_map(map_layout_json):
    tiles = get_random_tiles(map_layout_json)
    cities = get_random_cities(tiles)

    #make lists
    tiles = list(tiles.values())
    cities = list(cities.values())

    map = Map(cities, tiles)

    return map


def get_random_cities(tiles, city_layout_json = "map_generation/info/cities.json"):
    with open(city_layout_json, "r") as f:
        city_layout = json.load(f)

    cities = {}
    for pos, tiles_idx in city_layout.items():
        tmptiles = [tiles[i] for i in tiles_idx if i in tiles.keys()]
        if len(tmptiles) != 0:
            name = "_".join([str(v) for v in tiles_idx])
            cities[name] = City(pos, tmptiles)

    return cities

def get_random_tiles(map_layout_json):
    with open(map_layout_json, "r") as f:
        map_layout = json.load(f)

    #get lists of dice values, and resources
    dice_values = get_dice_values_list()
    resources = get_resource_list()



    assert len(map_layout) == 44
    assert len(resources) == 25
    assert len(dice_values) == 25


    #shuffle them to make a random map
    random.shuffle(dice_values)
    random.shuffle(resources)

    tiles = {}
    gold_dice_values = [3, 11]
    for position, tile_type in map_layout.items():
        position = int(position)

        if tile_type == "random":
            res = resources.pop()
            dval = int(dice_values.pop())

            t = Tile(position, res, dval)
            tiles[position] = t

        elif tile_type == "gold":
            dval = gold_dice_values.pop()
            res = "gold"

            t = Tile(position, res, dval)
            tiles[position] = t

        elif tile_type == "water":
            t = Tile(position, resource = "water", dice_value = None)
            tiles[position] = t


    return tiles


#helper functions
def get_dice_values_list():
    with open("map_generation/info/dice_values.json", "r") as f:
        dice_dict = json.load(f)

    dice_list = []
    for key in dice_dict:
        if key != "gold":
            dice_list += [int(key)]*dice_dict[key]

    count = {i: dice_list.count(str(i)) for i in range(2, 13)}

    return dice_list

def get_resource_list():
    with open("map_generation/info/resources.json", "r") as f:
        tiles_dict = json.load(f)

    tile_list = []
    for key in tiles_dict:
        if key != "gold":
            tile_list += [key]*tiles_dict[key]

    return tile_list
