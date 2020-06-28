class Tile:
    def __init__(self, position, resource, dice_value):
        self.position = int(position)
        self.resource = resource
        self.dice_value = dice_value
        self.probability = (6-abs(int(dice_value)-7))/36 if self.dice_value  else 0


    def info(self):
        print("-"*20)
        print("position: ", self.position)
        print("resource: ", self.resource)
        print("dice_value: ", self.dice_value)
        print("-"*20)

    def __repr__(self):
        return self.resource if self.resource is not None else "water"
