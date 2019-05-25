

class Tile:
    def __init__(self, position, resource, dice_value):
        self.position = position
        self.resource = resource
        self.dice_value = dice_value

    def info(self):
        print("-"*20)
        print("position: ", self.position)
        print("resource: ", self.resource)
        print("dice_value: ", self.dice_value)
        print("-"*20)
