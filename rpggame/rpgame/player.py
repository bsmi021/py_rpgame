from .utils import *
from .item import *


class Player(object):

    def __init__(self, player_id: int, name: str, level: int = 1):
        self.id: str = player_id
        self.instance_id = hash(uuid.uuid1())
        self.name: str = name
        self.level: int = level
        self.base_min_damage: int = 2
        self.base_max_damage: int = 8
        self.min_damage: int = 1
        self.max_damage: int = 8
        self.base_critical_chance: float = .05
        self.critical_chance: float = .05
        self.critical_multiplier: float = 2.5
        self.miss_chance: float = .05
        self.items: [] = []

    def _calc_min_damage(self):
        result = self.base_min_damage
        for e_item in self.items:
            result += round(e_item.attack_power / 4.75)
        self.min_damage = self.base_min_damage + result

    def _calc_max_damage(self):
        result = self.base_max_damage
        for e_item in self.items:
            result += round(e_item.attack_power / 2)
        self.max_damage = self.base_max_damage + result

    def _calc_critical_chance(self):
        result: float = self.base_critical_chance
        for e_item in self.items:
            result += e_item.crit_chance

        result = int(result * 100) * .01
        self.critical_chance = self.base_critical_chance + result

    def equip_items(self, equip_item: Item = None):
        """ Equips an item on the player so they're ready to fight """
        if equip_item is not None:
            for r_item in self.items:
                if r_item.equip_slot == equip_item.equip_slot:
                    self.items.remove(r_item)
                    self.items.append(equip_item)

            self.items.append(equip_item)

        self._calc_max_damage()
        self._calc_min_damage()
        self._calc_critical_chance()

    def __str__(self):
        return 'Name:{0.name}|Max_Attack:{0.max_damage}|' \
               'Min_Attack:{0.min_damage}|Crit_Chance:{0.critical_chance}' \
            .format(self)

    def get_json_string(self):
        equipped_items = []
        for x_item in self.items:
            equipped_items.append({'id': x_item.id, 'item_slot': x_item.equip_slot.value,
                                   'slot_name': x_item.equip_slot.name})

        obj = {
            'id': self.id,
            'instance_id': self.instance_id,
            'name': self.name,
            'level': self.level,
            'base_min_damage': self.base_min_damage,
            'base_max_damage': self.base_max_damage,
            'min_damage': self.min_damage,
            'max_damage': self.max_damage,
            'base_critical_chance': self.base_critical_chance,
            'critical_chance': self.critical_chance,
            'critical_multiplier': self.critical_multiplier,
            'miss_chance': self.miss_chance,
            'equipped_items': equipped_items
        }

        return jsonpickle.encode(obj, unpicklable=False)
        # result = '{{ "id":{0.id},' \
        #          '"instance_id":{0.instance_id},' \
        #          '"name":"{0.name}",' \
        #          '"level":{0.level},' \
        #          '"base_min_damage":{0.base_min_damage},' \
        #          '"base_max_damage":{0.base_max_damage},' \
        #          '"min_damage":{0.min_damage},' \
        #          '"max_damage":{0.max_damage},' \
        #          '"base_critical_chance":{0.base_critical_chance},' \
        #          '"critical_chance":{0.critical_chance},' \
        #          '"critical_multiplier":{0.critical_multiplier},' \
        #          '"miss_chance":{0.miss_chance},' \
        #          '"equipped_items":{1}}}'.format(self, e_items_str)
        #
        # return result


class Party(object):
    def __init__(self, name: str):
        self.id = hash(uuid.uuid1())
        self.name: str = name
        self.members: [] = []
        self.cr_date = get_localized_time()

    def add_party_member(self, player: Player):
        self.members.append(player)

    def get_json_string(self):
        party_members = []
        for p in self.members:
            party_members.append({'id': p.id, 'instance_id': p.instance_id})

        obj = {'id': self.id,
               'name': self.name,
               'cr_date': self.cr_date,
               'members': party_members}

        return jsonpickle.encode(obj, unpicklable=False)

    def __str__(self):
        party_members = []
        for p in self.members:
            p_instance_id = p.instance_id
            party_members.append(p_instance_id)

        members_json = json.dumps(party_members)

        result = "{{\"id\": {0.id}, \"name\": \"{0.name}\"," \
                 "\"create_date\": \"{0.cr_date}\"," \
                 "\"members\": {1}}}".format(self, members_json)

        return result
