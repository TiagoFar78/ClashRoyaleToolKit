from rarity import Rarity

class Card:
    def __init__(self, name, level, max_level, count):
        self.name = name
        self.level = level
        self.rarity = Rarity.get_rarity(max_level)
        self.count = count