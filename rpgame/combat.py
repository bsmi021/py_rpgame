import datetime
import random
import time

import confluent_kafka
import pytz

from rpgame import enemy, player


def get_attack_time():
    """ returns the timestamp of the attack"""
    utc_time = datetime.datetime.utcnow()
    return pytz.utc.localize(utc_time).astimezone()


def get_random_enemy() -> enemy.Enemy:
    enemy_rand = random.randint(1, 3)

    if enemy_rand == 2:
        i_enemy = enemy.Vampire(name='Vampire_{}'.format(hash(str(random.randint(0, 10000000)) + 'V')),
                                level=random.randint(1, 3))
    elif enemy_rand == 3:
        i_enemy = enemy.Orc(name='Orc_{}'.format(hash(str(random.randint(0, 10000000)) + 'O')),
                            level=random.randint(1, 5))
    else:
        i_enemy = enemy.Troll(name='Troll_{}'.format(hash(str(random.randint(0, 10000000)) + 'T')),
                              level=random.randint(1, 3))

    return i_enemy


class Fight(object):
    def __init__(self, party: player.Party, enemy: enemy.Enemy):
        self.party = party
        self.enemy = enemy
        self.attacks: [] = []
        self.is_fight_active: bool = False

    def kafka_produce_report(self, err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def start_fight(self, file_path: str = None, send_to_kafka: bool = False):
        self.is_fight_active = True
        while self.enemy.alive:
            party_member: int = random.randint(1, len(self.party.members)) - 1
            f_player: player.Player = self.party.members[party_member]

            attack = Attack(f_player, self.enemy)
            self.attacks.append(attack)
            # put an artificial break in the action
            time.sleep(random.randint(0, 35) * .01)
            attack.execute_attack()
            if file_path is None and not send_to_kafka:
                print(attack.get_log_entry())
            elif send_to_kafka:
                producer = confluent_kafka.Producer({'bootstrap.servers': '18.235.75.135'})
                kafka_topic: str = 'rpggame2_combat_log'

                kafka_message = attack.get_log_entry().rstrip('\n').strip().encode('utf-8')
                producer.produce(kafka_topic, kafka_message, callback=self.kafka_produce_report)
            else:
                with open(file_path, 'a') as log_file:
                    print(attack.get_log_entry(), file=log_file)
        else:
            self.is_fight_active = False

    def get_fight_summary(self):
        dodge_count: int = 0
        block_count: int = 0
        miss_count: int = 0
        total_block_amount: int = 0
        total_gross_damage: int = 0
        critical_count: int = 0
        total_net_damage: int = 0
        overkill_total: int = 0
        gross_attack_count: int = 0
        net_attack_count: int = 0

        for attack in self.attacks:
            if attack.was_dodged:
                dodge_count += 1

            if attack.was_blocked:
                block_count += 1

            if attack.was_missed:
                miss_count += 1

            total_block_amount += attack.amount_blocked
            total_gross_damage += attack.player_attack_amount
            total_net_damage += attack.player_attack_amount - attack.amount_blocked - attack.overkill  # - attack.overkill

            if attack.was_critical:
                critical_count += 1

            gross_attack_count += 1
            overkill_total += attack.overkill

            if not attack.was_dodged and not attack.was_missed:
                net_attack_count += 1

        print('*' * 40 + 'Fight Summary for {}'.format(attack.enemy.name) + '*' * 40)

        print('Enemy Orig. HP:{}'
              ' | Gross Dmg:{}'
              ' | Net Dmg:{}'
              ' | Blocked Dmg:{}'
              ' | Overkill:{}'
              ' | \n\tCritical Count:{}'
              ' | Gross Atk. Count:{}'
              ' | Net Atk. Count:{}'
              ' | Dodged:{}'
              ' | Misses:{}'
              ' | Blocked:{}'
              ' | Attack Success:{}'
              .format(attack.enemy.original_hit_points, total_gross_damage,
                      total_net_damage, -total_block_amount,
                      -overkill_total, critical_count,
                      gross_attack_count, net_attack_count,
                      dodge_count,
                      miss_count,
                      block_count,
                      float(net_attack_count / gross_attack_count) * 100))
        print('*' * 40 + '*' * 40)


class Attack(object):
    def __init__(self, i_player: player.Player, i_enemy: enemy.Enemy):
        """ Creates an instance of the Attack Class"""
        self._player: player.Player = i_player
        self._enemy: enemy.Enemy = i_enemy
        self._is_blocked: bool = False
        self._is_critical: bool = False
        self._is_parried: bool = False
        self._is_missed: bool = False
        self._is_dodged: bool = False
        self._base_attack: int = 0
        self._player_attack_amt: int = 0
        self.event_time: str = ''
        self.amount_blocked: int = 0
        self._is_reborn: bool = False
        self.overkill: int = 0

    # read only properties
    @property
    def player_attack_amount(self) -> int:
        return self._player_attack_amt

    @property
    def was_dodged(self) -> bool:
        return self._is_dodged

    @property
    def was_parried(self) -> bool:
        return self._is_parried

    @property
    def was_blocked(self) -> bool:
        return self._is_blocked

    @property
    def was_critical(self) -> bool:
        return self._is_critical

    @property
    def was_missed(self) -> bool:
        return self._is_missed

    @property
    def is_dead(self) -> bool:
        return not self._enemy.alive

    @property
    def was_reborn(self) -> bool:
        return self._is_reborn

    @property
    def player(self) -> player.Player:
        return self._player

    @property
    def enemy(self) -> enemy.Enemy:
        return self._enemy

    @staticmethod
    def get_attack_time():
        """ returns the timestamp of the attack"""
        utc_time = datetime.datetime.utcnow()
        return pytz.utc.localize(utc_time).astimezone()

    @staticmethod
    def calc_critical(f_critical_chance: float = 0.0) -> bool:
        """Returns a true or false after calculating if the attack was a critical or not

        Args:
            f_critical_chance (float): represents the player's critical strike chance
            """
        return (random.randint(1, 100) * .01) <= f_critical_chance

    def execute_attack(self):
        """ Executes the attack, this will call player_attack() and take_damage()
            which will carry out calculating the base player attack information
            and then the enemy action"""
        self._enemy.previous_hp = self._enemy.hit_points
        self._calc_attack()
        self._attack_target()

    def _calc_attack(self):
        """ Calculates the attack amount, will determine if the attack was missed which
            will result in 0 attack amount or crit which will multiply the attack amount
            by 1.5 times."""

        self._is_missed = self._calc_missed()

        # check to see if the attack was missed outright no need to go much further if so
        if self._is_missed:
            return

        # get the base attack value for the player
        self._base_attack = random.randint(self._player.min_damage, self._player.max_damage)
        self._player_attack_amt = self._base_attack

        # work out the critical strike chance
        self._is_critical = Attack.calc_critical(self._player.critical_chance)
        if self._is_critical:
            self._player_attack_amt *= 1.5

        self._player_attack_amt = round(self._player_attack_amt)

    def _attack_target(self):
        """ Processes damage from a player to an enemy"""

        self.event_time = self.get_attack_time()

        if self.was_missed:
            return

        if not self._enemy.alive:
            return

        t_enemy = self._enemy

        # if the enemy can dodge check to see if the attack was dodged
        if t_enemy.can_dodge:
            self._is_dodged = self._calc_dodges()
            if self._is_dodged:
                # if the target dodged they will take no damage
                # move out of method
                self.overkill = 0
                self._player_attack_amt = 0
                # bail out if the attack was dodged nothing more to do
                return

        # if the enemy can block attacks check to see if attack was blocked
        # if the attack was blocked take the amount of the blocked attack from the attack amount
        # even if the attack was blocked there will still be damage this is based on the enemy's
        # the product of the player's attack by the block amount
        if t_enemy.can_block:
            self._is_blocked = self._calc_blocked()
            if self._is_blocked:
                self.amount_blocked = round(self.player_attack_amount * t_enemy.block_amount)

        # get the effective attack amount this is player_attack_amount take amount_blocked
        effective_attack: int = self.player_attack_amount - self.amount_blocked

        # get the remaining hit points this is the hit points take the effective attack
        # this number can be negative due to overkill
        remaining_points: int = t_enemy.hit_points - effective_attack

        self.overkill = effective_attack - t_enemy.hit_points

        # overkill cannot be negative, it will be 0 or the actual overkill value
        if self.overkill < 0:
            self.overkill = 0

        if remaining_points > 0:
            t_enemy.hit_points = remaining_points
        elif not t_enemy.alive:
            self.overkill = effective_attack
            return
            # print('You\'re beating on a corpse, knock it off')
        else:
            # the enemy is dead their hit points should be 0 and they're marked as not alive
            t_enemy.hit_points = 0
            t_enemy.alive = False

            # Rebirth logic, we'll come back to this later
            # t_enemy.lives -= 1
            #
            # if t_enemy._can_rebirth and t_enemy.lives > 0:
            #     if (random.randint(1, 100) * .001) <= t_enemy._rebirth_chance:
            #         if t_enemy.alive:
            #             t_enemy.hit_points = t_enemy._original_hp
            #             self._is_reborn = True
            # else:

    def _calc_blocked(self):
        """ Determines if an attack is blocked this is based on the enemies block chance"""
        return random.randint(1, 100) * .01 <= self._enemy._block_chance

    def _calc_dodges(self):
        """ Determines if an attack is dodged based on enemy's dodge chance """
        return random.randint(1, 100) * .01 <= self._enemy._dodge_chance

    def _calc_missed(self):
        """ Determines if a player's strike will miss based on his miss_chance """
        return (random.randint(1, 100) * .01) <= self._player.miss_chance

    def get_log_entry(self) -> str:
        result: str = '' \
                      '{0.event_time}|{0.player.name}|{0.enemy.name}|' \
                      '{0.enemy.level}|{0.enemy.original_hit_points}|' \
                      '{0.enemy.previous_hp}|{0.enemy.hit_points}|' \
                      '{0.player_attack_amount}|{0._base_attack}|' \
                      '{0.overkill}|{0.was_critical}|{0.was_missed}|{0.was_blocked}|' \
                      '{0.was_dodged}|{0.amount_blocked}|{0.is_dead}' \
            .format(self)

        return result

    # def __str__(self):
    #     return '{0.event_time}|{0._player.name}|{0._enemy.name}|{0._enemy.level}' \
    #            '|Original HP:{0._enemy.original_hit_points}|Previous HP:{0._enemy.previous_hp}|' \
    #            'Current HP:{0._enemy.hit_points}' \
    #            '|Amount:{0.player_attack_amount}|Base Amount:{0._base_attack}|Overkill:{0.overkill}' \
    #            '|Critical:{0.was_critical}|Missed:{0.was_missed}|Blocked:{0.was_blocked}' \
    #            '|Dodged:{0.was_dodged}|Amount Blocked:{0.amount_blocked}|Is_Dead:{0.is_dead}' \
    #            '|Is_Reborn={0.was_reborn}' \
    #         .format(self)
