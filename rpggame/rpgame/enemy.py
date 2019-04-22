import uuid

import jsonpickle


class Enemy(object):
    def __init__(self, name: str = 'Enemy', hit_points: int = 0, level: int = 1,
                 can_block: bool = False, can_dodge: bool = False, can_parry: bool = False,
                 race: str = None):
        self.id = hash(uuid.uuid4())
        self.name = '{}[{}]'.format(name, level)
        self.hit_points: int = round(((hit_points * (1 + level * .1)) * 25.5))
        self.original_hit_points: int = self.hit_points
        self.previous_hp: int = self.hit_points
        self.race = race
        self.alive = True
        self.level = level
        self.experience_worth: int = round(10 * (1 + level) * 13.5)
        self.gold_value = round((.000000001 * ((1.632 + level) * 1000000)), 4)
        self.can_block = can_block
        self.can_dodge = can_dodge
        self.can_parry = can_parry
        self.block_chance = .18
        self.block_amount = .57
        self.dodge_chance = .08
        self.parry_chance = .05

    def __str__(self):
        return 'Name: {0.name}, Lives: {0.lives}, Hit Points: {0.hit_points}'.format(self)

    def get_json_string(self):
        return jsonpickle.encode(self, unpicklable=False)


class Troll(Enemy):
    def __init__(self, name: str, level: int = 1):
        super().__init__(name=name, hit_points=365, level=level, can_block=True, race='Troll')

    def grunt(self):
        """ Makes him say his name"""
        print('Ya\'mon me {0.name}, kill you'.format(self))


class Orc(Enemy):
    def __init__(self, name: str, level: int):
        super().__init__(name=name, hit_points=485, level=level, can_dodge=True, can_block=True, race='Orc')


class Gnoll(Enemy):
    def __init__(self, name: str, level: int):
        super().__init__(name=name, hit_points=317, level=level, can_dodge=True, race='Gnoll')
