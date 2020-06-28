import os

def select_map_layout(path = "map_layouts/"):
    layout_jsons = os.listdir(path)

    for i, json in enumerate(layout_jsons):
        print(f"[{i}] {json}")

    idx = int(input("what map_layout do you want to play?"))
    return path+layout_jsons[idx]
