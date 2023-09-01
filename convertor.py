from card import Card

class Convertor:
    @staticmethod
    def to_card(o):
        name = o.get("name")
        level = o.get("level")
        max_level = o.get("maxLevel")
        count = o.get("count")

        if name is None or level == 0 or max_level == 0:
            return None

        return Card(name, level, max_level, count)