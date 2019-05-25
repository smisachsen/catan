import random
import json

from city import City
from tile import Tile
from map import Map


def get_random_map():
    tiles = get_random_tiles()
    cities = get_random_cities(tiles)
    map = Map(cities, tiles)
    return map

def get_random_cities(tiles):
    with open("map_generation/info/cities.json", "r") as f:
        city_layout = json.load(f)

    cities = {}
    for pos, tiles_idx in city_layout.items():
        tmptiles = [tiles[i] for i in tiles_idx if i in tiles.keys()]
        if len(tmptiles) != 0:
            name = "_".join([str(v) for v in tiles_idx])
            cities[name] = City(pos, tmptiles)

    return cities

def get_random_tiles():
    with open("map_generation/info/map_layout.json", "r") as f:
        map_layout = json.load(f)

    #get lists of dice values, and resources
    dice_values = get_dice_values_list()
    resources = get_resource_list()

    #shuffle them to make a random map
    random.shuffle(dice_values)
    random.shuffle(resources)

    tiles = {}
    idx = 0
    for position, tile_type in map_layout.items():
        position = int(position)
        if tile_type == "random":
            res = resources[idx]
            dval = dice_values[idx]
            idx += 1

            t = Tile(position, res, dval)
            tiles[position] = t

        elif tile_type == "gold":
            if position == 4:
                dval = 3
            elif position == 41:
                dval == 11
            res = "gold"


            t = Tile(position, res, dval)
            tiles[position] = t

    return tiles


#helper functions
def get_dice_values_list():
    with open("map_generation/info/dice_values.json", "r") as f:
        dice_dict = json.load(f)

    dice_list = []
    for key in dice_dict:
        dice_list += [key]*dice_dict[key]

    return dice_list

def get_resource_list():
    with open("map_generation/info/resources.json", "r") as f:
        tiles_dict = json.load(f)

    tile_list = []
    for key in tiles_dict:
        tile_list += [key]*tiles_dict[key]

    return tile_list
