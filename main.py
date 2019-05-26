import json


from map_generation.filtrate_maps import search_for_maps

N = 1_000
maps = list(search_for_maps(N = N))

for i, map in enumerate(maps):
    print("map ", i)
    map.info()
    print()

map_idx = int(input("what map do you want to play?"))
maps[map_idx].print_layout()
