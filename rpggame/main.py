import csv
import random
import os
from collections import namedtuple
from multiprocessing import Process

from rpgame import combat, player
from rpgame.item import Item, ItemSlot
from rpgame.utils import *


def run_fight_sim(f_fight: combat.Fight, f_send_to_kafka: bool):
    """ Executes the fight logic allowing multiple fights to occur at once"""
    f_producer = None
    if f_send_to_kafka:
        f_producer = kafka_get_producer()
    print(f_fight.start_fight(send_to_kafka=f_send_to_kafka, file_path=None, producer=f_producer))


def main():
    fight_count = 50
    send_to_kafka = True
    kafka_producer = None

    print('Starting to process {} fights, please be patient...'.format(fight_count))

    if send_to_kafka:
        kafka_producer = kafka_get_producer()

    # set the collections used by the program
    data = []
    players: [] = []
    parties: [] = []
    enemies: [] = []
    items = []

    # specify the fields for the player.txt import file
    player_fields = 'id', 'name', 'level', 'head', 'chest', 'shoulders', 'legs', \
                    'wrist', 'hands', 'feet', 'back', 'main_hand', \
                    'off_hand', 'both_hand'

    player_item = namedtuple('player_item', " ".join(player_fields))

    # import the items collection from the data\items.txt file
    # for each line create a new instance of Item and add it to the items list
    with open(os.path.join('data', 'items.txt'), 'r', newline='') as infile:
        reader = csv.reader(infile, delimiter='|')
        for row in reader:  # need to skip the first row since there is a header
            if row[0].strip() == "id":
                continue

            item = Item(id=int(row[0]),
                        name=row[1].strip(),
                        attack_power=int(return_0_if_none(row[2].strip())),
                        crit_chance=float(row[3]),
                        slot=ItemSlot(int(row[4])))
            items.append(item)

    # import the players collection from data\players.txt file
    # for each line in the file parse it and Player and add it to the temporary namedtuple list
    with open(os.path.join('data', 'players.txt'), 'r', newline='') as infile:
        reader = csv.reader(infile, delimiter='|')
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

    # create a player record for each player
    for p_data in data:
        playr = player.Player(player_id=int(p_data.id), name=p_data.name, level=p_data.level)
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
        if send_to_kafka:
            kafka_produce_message(kafka_producer, player_topic, playr.get_json_string())
            print('Player Registered:\n {0}'.format(playr.get_json_string()))
        else:
            print(playr.get_json_string())

    # create parties for the players, players are selected randomly and assigned to a party
    # note that players can only appear in one party per execution of the program
    for i in range(5):
        party = player.Party('Party')
        party.name = party.id  # renaming the party by its ID, don't need a special name for this
        parties.append(party)
        while len(players) > 0 \
                and len(party.members) <= 3:
            party.add_party_member(players.pop(random.randint(0, len(players) - 1)))
        if send_to_kafka:
            kafka_produce_message(kafka_producer, party_topic, party.get_json_string())
            print('Party Registered:\n {0}'.format(party.get_json_string()))
        else:
            print(party.get_json_string())

    """ Simulate :fight_count fights:
            Create a random Enemy
            Select one of the parties from the parties list
            Create a fight object (file_path will write the combat log
            Get the fight summary on the screen
    """
    for i in range(fight_count):
        enemy = combat.get_random_enemy()
        if send_to_kafka:
            kafka_produce_message(kafka_producer, enemy_topic, enemy.get_json_string())
            print('Enemy Registered:\n {0}'.format(enemy.get_json_string()))
        else:
            print(enemy.get_json_string())

        party = parties[random.randint(0, len(parties) - 1)]
        fight = combat.Fight(party, enemy)

        if send_to_kafka:
            kafka_produce_message(kafka_producer, fight_topic, fight.get_json_string())
            print('Fight Registered:\n {0}'.format(fight.get_json_string()))
        else:
            print(fight.get_json_string())

        Process(target=run_fight_sim, args=(fight, send_to_kafka)).start()


if __name__ == '__main__':
    main()
