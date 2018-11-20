from rpgame import item


class Player(object):

    def __init__(self, name: str):
        self.name: str = name
        self._level: int = 1
        self._base_min_damage: int = 2
        self._base_max_damage: int = 8
        self._min_damage: int = 1
        self._max_damage: int = 8
        self.critical_chance_base: float = .08
        self._critical_chance: float = .08
        self.critical_multiplier: float = 2.5
        self.miss_chance: float = .05
        self.items: [] = []

    @property
    def min_damage(self) -> int:
        result = self._base_min_damage
        for e_item in self.items:
            result += round(e_item.attack_power / 5.8)

        # self._min_damage = result
        return result

    @property
    def max_damage(self) -> int:
        result = self._base_max_damage
        for e_item in self.items:
            result += round(e_item.attack_power / 2)
        # self._max_damage = result
        return result

    @property
    def critical_chance(self) -> float:
        result: float = self.critical_chance_base
        for e_item in self.items:
            result += e_item.crit_chance

        return result

    def equip_items(self, equip_item: item.Item = None):
        """ Equips an item on the player so they're ready to fight """
        if equip_item is not None:
            self.items.append(equip_item)

    def __str__(self):
        return 'Name:{0.name}|Max_Attack:{0.max_damage}|' \
               'Min_Attack:{0.min_damage}|Crit_Chance:{0.critical_chance}'\
            .format(self)

class Party(object):
    def __init__(self, name: str):
        self.name: str = name
        self.members: [] = []

    def add_party_member(self, player: Player):
        self.members.append(player)
