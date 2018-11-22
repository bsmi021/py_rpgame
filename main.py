import csv
import random
from collections import namedtuple

from rpgame import combat, player
from rpgame.item import Item, ItemSlot


def return_0_if_none(value_check):
    """ General function to return 0 if an int is null """
    if value_check is None or value_check is '':
        return 0
    else:
        return value_check


if __name__ == '__main__':

    data = []
    players: [] = []
    parties: [] = []
    enemies: [] = []
    items = []

    player_fields = 'id', 'name', 'level', 'head', 'chest', 'shoulders', 'legs', \
                    'wrist', 'hands', 'feet', 'back', 'main_hand', \
                    'off_hand', 'both_hand'

    player_item = namedtuple('player_item', " ".join(player_fields))

    with open('data\\items.txt', 'r', newline='') as infile:
        reader = csv.reader(infile, delimiter='|')
        for row in reader:
            if row[0].strip() == "id":
                continue

            item = Item(id=int(row[0]),
                        name=row[1].strip(),
                        attack_power=int(return_0_if_none(row[2].strip())),
                        crit_chance=float(row[3]),
                        slot=ItemSlot(int(row[4])))
            items.append(item)

    with open('data\\players.txt', 'r', newline='') as infile:
        reader = csv.reader(infile, delimiter='|')
        # get names from column headers
        for row in reader:
            # print(row)
            if row[0].strip() == 'id':
                continue
            data.append(player_item(id=int(row[0].strip()),
                                    name=row[1].strip(),
                                    level=int(row[2].strip()),
                                    head=return_0_if_none(row[3]),
                                    chest=return_0_if_none(row[4]),
                                    shoulders=return_0_if_none(row[5]),
                                    legs=return_0_if_none(row[6]),
                                    wrist=return_0_if_none(row[7]),
                                    hands=return_0_if_none(row[8]),
                                    feet=return_0_if_none(row[9]),
                                    back=return_0_if_none(row[10]),
                                    main_hand=return_0_if_none(row[11]),
                                    off_hand=return_0_if_none(row[12]),
                                    both_hand=return_0_if_none(row[13])
                                    ))

    for p_data in data:
        playr = player.Player(name=p_data.name, level=p_data.level)
        playr.equip_items(items[int(p_data.head) - 1])
        playr.equip_items(items[int(p_data.chest) - 1])
        playr.equip_items(items[int(p_data.shoulders) - 1])
        playr.equip_items(items[int(p_data.legs) - 1])
        playr.equip_items(items[int(p_data.wrist) - 1])
        playr.equip_items(items[int(p_data.hands) - 1])
        playr.equip_items(items[int(p_data.feet) - 1])
        playr.equip_items(items[int(p_data.back) - 1])
        playr.equip_items(items[int(p_data.both_hand) - 1])
        players.append(playr)

    # create parties for the players, players are selected randomly
    for i in range(5):
        party = player.Party('Party')
        parties.append(party)
        while len(players) > 0 \
                and len(party.members) <= 3:
            party.add_party_member(players.pop(random.randint(0, len(players) - 1)))

    # print out the party members
    for party in parties:
        print()
        print(party.name)
        for player in party.members:
            print(player)

    print()
    print()
    """ Simulate 25 fights:
            Create a random Enemy
            Select one of the parties from the parties list
            Create a fight object (file_path will write the combat log
            Get the fight summary on the screen
    """
    for i in range(0, 3000):
        enemy = None
        fight = None
        enemy = combat.get_random_enemy()
        party = parties[random.randint(0, len(parties) - 1)]
        fight = combat.Fight(party, enemy)
        fight.start_fight(send_to_kafka=True)#file_path='..\data\combat_log.out')
        #fight.get_fight_summary()
