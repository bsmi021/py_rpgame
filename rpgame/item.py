from enum import Enum


class ItemSlot(Enum):
    HEAD = 1
    CHEST = 2
    SHOULDERS = 3
    LEGS = 4
    WRIST = 5
    HANDS = 6
    FEET = 7
    BACK = 8
    NONE = 0
    MAIN_HAND = 9
    OFF_HAND = 10
    BOTH_HAND = 11


class Item(object):
    def __init__(self, name: str, attack_power: int, crit_chance: float = 0.0, slot: ItemSlot = ItemSlot.NONE):
        self.name = name
        self.attack_power = attack_power
        self.crit_chance: float = crit_chance
        self.equip_slot: ItemSlot = slot
