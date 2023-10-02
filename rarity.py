class Rarity:
    COMMON_MAX_LEVEL = 14
    RARE_MAX_LEVEL = 12
    EPIC_MAX_LEVEL = 9
    LEGENDARY_MAX_LEVEL = 6
    CHAMPION_MAX_LEVEL = 4

    COMMON_GOLD_TO_LEVEL_UP = [5, 20, 50, 150, 400, 1000, 2000, 4000, 8000, 15000, 35000, 75000, 100000]
    RARE_GOLD_TO_LEVEL_UP = [50, 150, 400, 1000, 2000, 4000, 8000, 15000, 35000, 75000, 100000]
    EPIC_GOLD_TO_LEVEL_UP = [400, 2000, 4000, 8000, 15000, 35000, 75000, 100000]
    LEGENDARY_GOLD_TO_LEVEL_UP = [5000, 15000, 35000, 75000, 100000]
    CHAMPION_GOLD_TO_LEVEL_UP = [35000, 75000, 100000]

    COMMON_CARDS_AMOUNT_TO_LEVEL_UP = [2, 4, 10, 20, 50, 100, 200, 400, 800, 1000, 1500, 3000, 5000]
    RARE_CARDS_AMOUNT_TO_LEVEL_UP = [2, 4, 10, 20, 50, 100, 200, 400, 500, 750, 1250]
    EPIC_CARDS_AMOUNT_TO_LEVEL_UP = [2, 4, 10, 20, 40, 50, 100, 200]
    LEGENDARY_CARDS_AMOUNT_TO_LEVEL_UP = [2, 4, 6, 10, 20]
    CHAMPION_CARDS_AMOUNT_TO_LEVEL_UP = [1, 2, 8, 10]

    def __init__(self, max_level, gold_to_level_up, cards_amount_to_level_up):
        self.max_level = max_level
        self.gold_to_level_up = gold_to_level_up
        self.cards_amount_to_level_up = cards_amount_to_level_up
        
    def isOnMaxLevel(self, level):
        return level >= self.max_level
        
    def getCardsAmountToLevelUp(self, level):
        return self.cards_amount_to_level_up[level - 1]
        
    def getGoldToLevelUp(self, level):
        return self.gold_to_level_up[level - 1]

    @staticmethod
    def get_rarity(max_level):
        if max_level == Rarity.COMMON_MAX_LEVEL:
            return Rarity(Rarity.COMMON_MAX_LEVEL, Rarity.COMMON_GOLD_TO_LEVEL_UP, Rarity.COMMON_CARDS_AMOUNT_TO_LEVEL_UP)
        elif max_level == Rarity.RARE_MAX_LEVEL:
            return Rarity(Rarity.RARE_MAX_LEVEL, Rarity.RARE_GOLD_TO_LEVEL_UP, Rarity.RARE_CARDS_AMOUNT_TO_LEVEL_UP)
        elif max_level == Rarity.EPIC_MAX_LEVEL:
            return Rarity(Rarity.EPIC_MAX_LEVEL, Rarity.EPIC_GOLD_TO_LEVEL_UP, Rarity.EPIC_CARDS_AMOUNT_TO_LEVEL_UP)
        elif max_level == Rarity.LEGENDARY_MAX_LEVEL:
            return Rarity(Rarity.LEGENDARY_MAX_LEVEL, Rarity.LEGENDARY_GOLD_TO_LEVEL_UP, Rarity.LEGENDARY_CARDS_AMOUNT_TO_LEVEL_UP)
        elif max_level == Rarity.CHAMPION_MAX_LEVEL:
            return Rarity(Rarity.CHAMPION_MAX_LEVEL, Rarity.CHAMPION_GOLD_TO_LEVEL_UP, Rarity.CHAMPION_CARDS_AMOUNT_TO_LEVEL_UP)