from map_generation.filtrate_maps import search_for_maps
from map_generation.create_island import write_island_to_json
from map_generation.utils import select_map_layout

import sys

N = 10_000

if len(sys.argv) > 1:
    use_old_map_layout = True
    num_islands = int(sys.argv[1])
    map_layout_json = sys.argv[2]
    write_island_to_json(num_islands, map_layout_json)

else:
    use_old_map_layout = False
    map_layout_json = select_map_layout()





maps = list(search_for_maps(N = N, map_layout_json = map_layout_json))
if len(maps) == 0:
    print("Didnt find any maps")
    sys.exit()

print("found maps: ", len(maps))
maps = sorted(maps, reverse = True)



for i, map in enumerate(maps):
    print("map ", i)
    map.info()
    print()

map_idx = int(input("what map do you want to play?"))
maps[map_idx].print_layout()
