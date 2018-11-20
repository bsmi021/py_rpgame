class Item(object):
    def __init__(self, name: str, attack_power: int, crit_chance: float = 0.0):
        self.name = name
        self.attack_power = attack_power
        self.crit_chance: float = crit_chance
