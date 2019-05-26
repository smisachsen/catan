

class Tile:
    def __init__(self, position, resource, dice_value):
        self.position = int(position)
        self.resource = resource
        self.dice_value = int(dice_value)
        self.probability = (6-abs(int(dice_value)-7))/36



    def info(self):
        print("-"*20)
        print("position: ", self.position)
        print("resource: ", self.resource)
        print("dice_value: ", self.dice_value)
        print("-"*20)
