

class City:
    def __init__(self, position, tiles):
        self.position = position
        self.tiles = tiles

    def info(self):
        print("-"*20)
        print("city position: ", self.position)
        print("-"*20)
