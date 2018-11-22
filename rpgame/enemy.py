class Enemy(object):
    def __init__(self, name: str = 'Enemy', hit_points: int = 0, lives: int = 1, level: int = 1,
                 can_block: bool = False, can_dodge: bool = False, can_parry: bool = False,
                 can_rebirth: bool = False):
        self._name = name
        self.hit_points: int = round(((hit_points * (1 + level * .1)) * 1.5))
        self._original_hp: int = self.hit_points
        self.previous_hp: int = self.hit_points

        self.lives = lives
        self.alive = True
        self.level = level
        self._experience_worth: int = round(10 * (1 + level) * 13.5)
        self._gold_value = round((.000000001 * ((1.632 + level) * 1000000)), 4)
        self._can_block = can_block
        self._can_dodge = can_dodge
        self._can_parry = can_parry
        self._block_chance = .18
        self._block_amount = .57
        self._dodge_chance = .08
        self._parry_chance = .05
        self._can_rebirth: bool = can_rebirth
        self._rebirth_chance = .013

    @property
    def original_hit_points(self) -> int:
        return self._original_hp

    @property
    def block_amount(self) -> float:
        return self._block_amount

    @property
    def max_hit_points(self) -> int:
        return self._original_hp

    @property
    def can_parry(self) -> bool:
        return self._can_parry

    @property
    def can_dodge(self) -> bool:
        return self._can_dodge

    @property
    def can_block(self) -> bool:
        return self._can_block

    @property
    def name(self):
        return '{0._name}[{0.level}]'.format(self)

    def __str__(self):
        return 'Name: {0.name}, Lives: {0.lives}, Hit Points: {0.hit_points}'.format(self)


class Troll(Enemy):
    def __init__(self, name: str, level: int = 1):
        super().__init__(name=name, lives=1, hit_points=365, level=level, can_block=True)

    def grunt(self):
        """ Makes him say his name"""
        print('Ya\'mon me {0.name}, kill you'.format(self))


class Orc(Enemy):
    def __init__(self, name: str, level: int):
        super().__init__(name=name, lives=3, hit_points=485, level=level, can_dodge=True, can_block=True)


class Vampire(Enemy):
    def __init__(self, name: str, level: int):
        super().__init__(name=name, lives=3, hit_points=317, level=level, can_dodge=True, can_rebirth=False)
