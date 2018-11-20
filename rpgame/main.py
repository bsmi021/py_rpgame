from rpgame import combat, player
from rpgame.item import Item

if __name__ == '__main__':
    party = []

    player_1 = player.Player('Osiris')
    party.append(player_1)

    player_1.equip_items(Item(name='bastard sword', attack_power=9, crit_chance=.03))
    player_1.equip_items(Item(name='hauberk of steel', attack_power=4, crit_chance=.02))
    player_1.equip_items(Item(name='bracers of handsomeness', attack_power=10, crit_chance=.01))
    player_1.equip_items(Item(name='cowl of the batman', attack_power=5, crit_chance=.02))
    player_1.equip_items(Item(name='slap-master sabatons', attack_power=4, crit_chance=.03))
    player_1.equip_items(Item(name='coif of vandals', attack_power=14, crit_chance=.035))

    player_2 = player.Player('Sandy')
    party.append(player_2)
    player_2.equip_items(Item(name='juggernaut maul', attack_power=12, crit_chance=.05))
    player_2.equip_items(Item(name='breastplate of might', attack_power=6, crit_chance=.04))
    player_2.equip_items(Item(name='bracers of might', attack_power=11, crit_chance=.01))
    player_2.equip_items(Item(name='cask of might', attack_power=6, crit_chance=.02))
    player_2.equip_items(Item(name='boots of might', attack_power=5, crit_chance=.01))
    player_2.equip_items(Item(name='death-dealer\'s great cloak', attack_power=16, crit_chance=.02))

    player_3 = player.Player('Oliver')
    party.append(player_3)
    player_3.equip_items(Item(name='thunder fury', attack_power=26, crit_chance=.08))
    player_3.equip_items(Item(name='judgement chest guard', attack_power=6, crit_chance=.04))
    player_3.equip_items(Item(name='judgement bracers', attack_power=8, crit_chance=.02))
    player_3.equip_items(Item(name='hood of judgement', attack_power=9, crit_chance=.04))
    player_3.equip_items(Item(name='judgement sabatons', attack_power=7, crit_chance=.02))
    player_3.equip_items(Item(name='light-bearer shawl', attack_power=6, crit_chance=.03))

    enemies = []

    for player in party:
        print(player)

    print()
    print()
    for i in range(0, 10):
        enemy = None
        fight = None
        enemy = combat.get_random_enemy()
        fight = combat.Fight(party, enemy)
        fight.start_fight(file_path='..\data\combat_log.out')
        fight.get_fight_summary()
