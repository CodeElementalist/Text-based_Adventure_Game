# You can use this workspace to write and submit your adventure game project.
import time
import random


def slow_print(string):
    print(string + "\n")
    time.sleep(2)


def valid_input(string, option_list, role, battle):
    player_input = input(string + "\n").lower()
    if player_input in option_list:
        return player_input
    else:
        if role == 1:
            slow_print("A noble warrior will read through the options"
                       " and  make his decision without playing trick!")
            return valid_input(string, option_list, role, battle)
        elif role == 2:
            if len(option_list) <= 5:
                new = random.randint(1, len(option_list))
                if battle:
                    slow_print("It seem like you casted the spell "
                               "incorrectly and end up casting "
                               f"'{option_list[new-1]}'!")
                else:
                    slow_print("Something wrong with your teleportation "
                               "magic and you are teleporting to a "
                               "unknown location!")
                return str(new)
            else:
                slow_print("You can't do magic for these thing!")
                return valid_input(string, option_list, role, battle)
        else:
            if battle:
                slow_print("You use some unusual fighting techniques!")
                return "-1"
            else:
                slow_print("You sneak around ... and found yourself "
                           "not doing anything useful ...")
                return valid_input(string, option_list, role, battle)


def valid_input2(string, role, endgame):
    player_input = input(string + "\n").lower()
    if player_input in ["y", "yes", "n", "no"]:
        if player_input == "y" or player_input == "yes":
            return "y"
        else:
            return "n"
    else:
        if endgame:
            return valid_input2(string, role, endgame)
        else:
            if role == 3:
                return "-1"
            else:
                return valid_input2(string, role, endgame)


def enemy_reset(counter):
    if counter[0] % 6 == 0:
        for count in range(len(counter)):
            if count != 0:
                counter[count] = True


def reward(items):
    n = random.randint(3, 6)
    items[0] += n
    slow_print(f"You received {n} gold")
    print(f"Your Gold:  {items[0]}\n")


def encounter(name_holder, player_attr, creature_attr, items, endgame):
    slow_print("You encounter an enemy")
    run = valid_input2("<Do you want to fight it? (y/n)>", name_holder[1],
                       False)
    if run == "y":
        fight(name_holder, player_attr, creature_attr, items,
              creature_attr[0], False)
    elif run == "n":
        if random.randint(0, 2) == 0:
            slow_print("Your disguise is exposed and the enemy attacked you!")
            fight(name_holder, player_attr, creature_attr, items,
                  creature_attr[0], False)
    else:
        if random.randint(0, 1) == 0:
            slow_print("Your reckless actions draw the enemy attention and "
                       "you are attacked!")
            fight(name_holder, player_attr, creature_attr, items,
                  creature_attr[0], False)
        else:
            n = random.randint(1, 6)
            if n == 1:
                if player_attr[0] > 100:
                    m = random.randint(1, 2)
                    player_attr[0] += m
                    slow_print("You stole a healing potion from your enemy "
                               "without being notice and heal yourself for "
                               f"{m} Hp.")
                    print(f"Your Hp: {player_attr[0]}\n")
                else:
                    slow_print("You get away safely ...")
            elif n == 4:
                if "dagger1" in items and "dagger2" not in items:
                    m = random.randint(1, 6)
                    if m == 4:
                        items.append("dagger2")
                        slow_print('You stole a "Thin Blade Dagger" from '
                                   'your enemy without being notice.')
                    else:
                        slow_print("You stole nothing from your enemy and "
                                   "get away safely ...")
                else:
                    slow_print("You get away safely ...")
            elif n == 6:
                m = random.randint(1, 2)
                items[0] += m
                slow_print(f"You stole {m} gold from your enemy without "
                           "being notice.")
                print(f"Your Gold:  {items[0]}\n")
            else:
                slow_print("You get away safely ...")


def fight(name_holder, player_attr, enemy_attr, items, enemy_hp_max,
          bossfight):
    if name_holder[1] == 1:
        skills = skill1(items)
    elif name_holder[1] == 2:
        skills = skill2(items)
    else:
        skills = skill3(items)
    unusual = 0
    turn = 0
    opt = []
    for num in range(len(skills)):
        opt.append(str(1 + num))
    enemy_total = [0, 0, 0]
    enemy_total[0] = enemy_attr[0]
    while player_attr[0] > 0 and enemy_total[0] > 0:
        if enemy_total[0] < int(enemy_hp_max * 0.3):
            enemy_total[1] = int(enemy_attr[1] * 1.2)
        else:
            enemy_total[1] = enemy_attr[1] + random.randint(0, 2)
        enemy_total[2] = enemy_attr[2]
        if bossfight:
            if turn % 6 == 5:
                enemy_total[1] += 150
                enemy_total[2] += 30
            if turn % 5 == 4:
                enemy_total[0] += 25
                print("The enemy heal itself for 25 Hp!\n")
            if turn % 3 == 2:
                enemy_total[2] += 40
            if turn % 2 == 1:
                enemy_total[1] += 30
        item_bonus = item_effect(name_holder, items)
        if len(skills) > 0:
            slow_print("What is your move!")
            for skill in range(len(skills)):
                print(f"{skill + 1}. {skills[skill]}")
            print("\n")
            skill_choice = valid_input("<Please enter a number.>", opt,
                                       name_holder[1], True)

            if name_holder[1] == 1:
                skill_bonus = skill1_effect(skill_choice, items,
                                            enemy_total[1], item_bonus)
            elif name_holder[1] == 2:
                skill_bonus = skill2_effect(skill_choice, items)
            elif name_holder[1] == 3:
                if skill_choice == "-1":
                    unusual += 1
                skill_bonus = skill3_effect(skill_choice, items, unusual)
        else:
            skill_bonus = [0, 0, 0]

        player_total = []
        for attr in range(3):
            player_total.append(player_attr[attr] + item_bonus[attr] +
                                skill_bonus[attr])
        player_total[1] += random.randint(1, 2)

        evaluate(enemy_total, player_total)
        player_attr[0] = player_total[0]

    if player_attr[0] > 0:
        reward(items)


def evaluate(enemy_total, player_total):
    p = player_total[1] - enemy_total[2]
    if p < 0:
        p = 0
    e = enemy_total[1] - player_total[2]
    if e < 0:
        e = 0
    enemy_total[0] -= p
    player_total[0] -= e
    if enemy_total[0] < 0:
        enemy_total[0] = 0
    if player_total[0] < 0:
        player_total[0] = 0
    if player_total[0] > 100:
        player_total[0] = 100

    slow_print(f"You deal {p} damage to your enemy and you received {e} "
               "damage.")
    print(f"Enemy HP: {enemy_total[0]}")
    print(f"Your HP: {player_total[0]}\n")


def item_effect(name_holder, items):
    if name_holder[1] == 1:
        if "weapon3" in items:
            atk = 20
        elif "weapon2" in items:
            atk = 12
        elif "weapon1" in items:
            atk = 7
        else:
            atk = 0

        if "shield3" in items:
            defen = 25
        elif "shield2" in items:
            defen = 15
        elif "shield1" in items:
            defen = 9
        else:
            defen = 0

        return [0, atk, defen]
    elif name_holder[1] == 2:
        return [0, 0, 0]
    elif name_holder[1] == 3:
        if "dagger2" in items:
            return [0, 8, 0]
        elif "dagger1" in items:
            return [0, 5, 0]
        else:
            return [0, 0, 0]


def skill1(items):
    skill_list = []
    for item in range(len(items)):
        if item != 0 and items[item][0:6] == "weapon":
            skill_list.append("Sword Slash")
            skill_list.append("Counter Slash")
            break
    for item in range(len(items)):
        if item != 0 and items[item][0:6] == "shield":
            skill_list.append("Shield Deflection")
            skill_list.append("Shield Block")
            break
    return skill_list


def skill1_effect(skill_choice, items, enemy_atk, item_bonus):
    W = False
    for item in range(len(items)):
        if item != 0 and items[item][0:6] == "weapon":
            W = True
            break

    if W:
        new_skill_choice = skill_choice
    else:
        if skill_choice == "1":
            new_skill_choice = "3"
        else:
            new_skill_choice = "4"

    if new_skill_choice == "1":
        if "weapon1" in items:
            atk = random.randint(7, 14) * random.randint(1, 2)
        elif "weapon2" in items:
            atk = random.randint(11, 20) * random.randint(1, 3)
        elif "weapon3" in items:
            atk = random.randint(16, 31) * random.randint(2, 4)
        defen = - int(item_bonus[2] / 2)
    elif new_skill_choice == "2":
        if "weapon1" in items:
            atk = random.randint(3, 11) * random.randint(1, 2)
            defen = random.randint(5, 7)
        elif "weapon2" in items:
            atk = random.randint(4, 13) * random.randint(1, 3)
            defen = random.randint(8, 10)
        elif "weapon3" in items:
            atk = random.randint(8, 18) * random.randint(2, 4)
            defen = random.randint(12, 15)
        defen -= int(item_bonus[2] / 3)
    elif new_skill_choice == "3":
        if "shield1" in items:
            atk = 1 * random.randint(1, 2)
            defen = random.randint(14, 18)
        elif "shield2" in items:
            atk = 3 * random.randint(1, 2)
            defen = random.randint(21, 38)
        elif "shield3" in items:
            atk = int(enemy_atk / 5)
            if int(enemy_atk / 2) < 50:
                n = 50
            else:
                n = int(enemy_atk / 2) + 10
            defen = random.randint(35, n)
        atk -= - int(item_bonus[1] / 2)
    elif new_skill_choice == "4":
        if "shield1" in items:
            defen = 25
        elif "shield2" in items:
            defen = 45
        elif "shield3" in items:
            defen = enemy_atk
        atk = - (item_bonus[1] + 5)
    return [0, atk, defen]


def skill2(items):
    skill_list = []
    for item in range(len(items)):
        if item != 0 and items[item][0:6] == "staff":
            skill_list.append("Sprit Channelling")
            skill_list.append("Elements Strike")
            skill_list.append("Light Barrier")
            skill_list.append("Real Illusion")
            break
    return skill_list


def skill2_effect(skill_choice, items):
    if "stone" in items:
        m = 2
    else:
        m = 1

    if "gem" in items:
        k = 3
    else:
        k = 1

    if skill_choice == "1":
        n = random.randint(-1, m + 1)
        hp = (n*4) + 1
        if n > -1:
            hp *= m
            atk = (random.randint((1 + n) * m, 20 * (m + 1))) * k
            slow_print(f"The skill heal you for {hp} Hp")
        else:
            atk = 0
            slow_print(f"The skill cost you {hp} Hp")
        defen = n * 2

    elif skill_choice == "2":
        n = random.randint(0, m + 3)
        hp = m - 2
        atk = (random.randint(m * m * m * 2, (25 + n) * m)) * n
        defen = random.randint((0 + m - 1) * (3 * m) * m, 15 * (n + m))
        slow_print(f"The skill cost you {hp} Hp")
    elif skill_choice == "3":
        n = random.randint(0, m + 2)
        hp = (random.randint(5 * m, 15 + 2 * m)) * n
        atk = 0
        defen = (random.randint(10 * m, 25 * m)) * n
        slow_print(f"The skill heal you for {hp} Hp")
    elif skill_choice == "4":
        n = random.randint(0, m + 1)
        hp = (random.randint(-2, 5 * m)) * n
        atk = (random.randint(5 * m, (7 + k) * m)) * (k - 1) * n
        defen = 1000 * n
        if hp > 0:
            slow_print(f"The skill heal you for {hp} Hp")
        else:
            slow_print(f"The skill cost you {hp} Hp")
        if n != 0:
            slow_print("The enemy attacked a illusion copy of you!")

    return [hp, atk, defen]


def skill3(items):
    skill_list = []
    for item in range(len(items)):
        if item != 0 and items[item][0:6] == "dagger":
            skill_list.append("Quick Strike")
            skill_list.append("Stealth Strike")
            break
    return skill_list


def skill3_effect(skill_choice, items, unusual):
    if "poison" in items:
        m = 5
    else:
        m = 0

    if skill_choice == "1":
        atk = (random.randint(7, 10) + m) * random.randint(5, 7)
        defen = random.randint(12, 18)
        if unusual >= 2 and random.randint(0, 1) == 1:
            atk += 50
    elif skill_choice == "2":
        atk = (random.randint(7, 10) + m)
        defen = 1000 * random.randint(0, 1) + 30
        if unusual >= 2 and random.randint(0, 1) == 1:
            atk *= m
    else:
        n = random.randint(1, 6)
        if n <= 2:
            return [0, 0, 0]
        elif n == 3:
            return [0, 5, 10]
        elif n == 4:
            k = random.randint(1, 6)
            if k <= 3:
                return [0, 10, 70]
            elif k == 4:
                return [0, 200, 0]
            else:
                return [0, 60, 160]
        elif n == 5:
            return [0, 0, 100]
        else:
            return [0, 20, 40]
    return [0, atk, defen]


def intro(name_holder):
    slow_print("You are doing some lab work alone at midnight in a "
               "university.")
    slow_print("When you are focusing to get the chemical mixture in "
               "the exact proportion, suddenly you heard someone banging "
               "on the lab door.")
    slow_print("You were shocked and accidently spill unknown amount of "
               "chemical to the mixture.")
    slow_print("The mixture flash a white light and you fainted......")
    slow_print("(Could it be an explosion???)")
    time.sleep(1)
    slow_print("When you regain your conscious, you find yourself in an "
               "unknown world!")
    weird_adj = random.choice(["bony", "buff", "lithe", "lanky", "lean",
                               "paunchy", "silly", "towering", "willowy",
                               "wiry"])
    animal1 = random.choice(["Lion", "Cheetah", "Bison", "Mammoth", "Cobra"])
    animal2 = random.choice(["dog", "horse", "bear", "turtle", "eagle",
                             "hawk"])
    slow_print(f"A {weird_adj} old man riding on a giant {animal1}-{animal2} "
               "is looking at you.")
    slow_print("The old man ask for your name.")
    name = input("<Please enter your name.>\n").upper()
    name_holder.append(name)


def role_select(name_holder):
    slow_print(f'\n"{name_holder[0]}?! What would you like to become? A '
               'noble mighty warrior? An unreliable but powerful magician?"')
    slow_print("""
    1. Noble Mighty Warrior
    2. Unreliable Powerful Magician
    """)
    player_choice = input("<Enter the number of your choice!> (Choose "
                          "wisely!)\n").lower()
    slow_print('\n"Ah ha! I knew it!!! You are the one that mentioned in '
               '"The Great Prophecy" to save us from the Evil Creature - '
               '"Dr. L"", he said.')
    if player_choice == "1" or "warrior" in player_choice:
        slow_print('"A noble man like you will face your enemies and take '
                   'them down with your courageous!"')
        slow_print('"Good equipment will certainly help you to accomplish '
                   'your mission."')
        name_holder.append(1)
    elif player_choice == "2" or "magician" in player_choice:
        slow_print('"A adventurous man like you will explore various '
                   'possible techniques and skills to take down your '
                   'enemies!"')
        slow_print('"Luck is essential when you explore or try something '
                   'new, although you may not agree with me, just mark my '
                   'word."')
        name_holder.append(2)
    else:
        slow_print('"A rebellious man who not listening nor following rules '
                   'and instructions."')
        slow_print('"You are definitely a disgraceful thief which I\'m not '
                   'sure how you could accomplish your mission.\"')
        slow_print('"However I have faith in you, just like I believe in '
                   '"The Great Prophecy""')
        slow_print('"When time has come, you will know that breaking the '
                   'rules are not always the best solution to a problem."')
        slow_print("A sudden thought come into his mind")
        slow_print('"Or ... maybe it could be a ways to beat Dr. L."')
        name_holder.append(3)
    slow_print("He give you a map and suggest you visit the village first.")
    slow_print("You have begun your adventure......")


def village(counter, name_holder, player_attr, items):
    if name_holder[1] != 2:
        slow_print("Within an hours, you have arrived the village's entrance.")
    else:
        slow_print("In a split second, you have teleported yourself to "
                   "the village's entrance.")

    enemy_reset(counter)

    if counter[1]:
        creature_attr = [50, 9, 1]  # hp,atk,def
        encounter(name_holder, player_attr, creature_attr, items, False)
        counter[1] = False

    if player_attr[0] != 0:
        slow_print("There are some villages and a shop.")
        slow_print("What would you do?")
        slow_print("""
        1. Talk to the villagers
        2. Enter the shop
        3. Go to the lakeside nearby the village
        4. Go inside the forest
        """)
        player_choice = valid_input("<Please enter the number of your "
                                    "choice.>", ["1", "2", "3", "4"],
                                    name_holder[1], False)

        if player_choice == "1":
            vill_tlk(counter, name_holder, player_attr, items)
        elif player_choice == "2":
            shop(counter, name_holder, player_attr, items)
        elif player_choice == "3":
            counter[0] += 1
            lake(counter, name_holder, player_attr, items)
        else:
            counter[0] += 1
            forest(counter, name_holder, player_attr, items)


def vill_tlk(counter, name_holder, player_attr, items):
    if name_holder[1] != 2:
        slow_print("Within a few minutes, you have approached the villagers.")
    else:
        slow_print("in a blink of an eye, you have teleported nearby the "
                   "villagers.")
        slow_print("They are amazed by your magic ...")
    if "Q1" not in items:
        slow_print(f"Hi you must be {name_holder[0]}, the one that come to "
                   "save us.")
        slow_print("You probably should visit the shop in the village to "
                   "gear you up a bit before you could face Dr. L.")

    if name_holder[1] == 1:
        if ("Q1" in items and ("iron" not in items or "copper" not in items
                               or "silver" not in items) and "Q2" not in items
                and "Q3" not in items and "Q4" not in items and "Q5" not in
                items):
            slow_print("You ask one of the villager where could you find "
                       "those ores that the shopkeeper seek.")
            slow_print("They told you that you might get some at the "
                       "lakeside or in the mountain.")
            if "copper" not in items:
                slow_print('"I found some weird stones lately and it might '
                           'be one of those you looking for", one young '
                           'villager said.')
                slow_print('"I would happy to give it to you free-of-charge '
                           'so that you could fulfil your quest!"')
                items.append("copper")
                slow_print('You received a "Copper" ore!')
            slow_print("You thanks the villagers and continue your quest ...")
    elif name_holder[1] == 2:
        if ("Q1" in items and ("leaf" not in items or "bone" not in items) and
                "gem" not in items):
            slow_print("You ask one of the villager where could you find "
                       "those materials that lead to sacred items.")
            slow_print("They told you that you might get some in the forest "
                       "or in the cave inside the mountain.")
            slow_print("You thanks the villagers and continue your quest ...")
    else:
        if "Q1" in items and ("leaf" not in items or "root" not in items or
                              "flower" not in items) and "poison" not in items:
            slow_print("You ask one of the villager where could you find "
                       "those herbs to produce poison.")
            slow_print("They told you that you might get some in the forest.")
            slow_print("You thanks the villagers and continue your quest ...")
    slow_print("You just chit-chatting with the villagers to pass time.")
    slow_print("The villagers remind you that you could also have medical "
               "treatment at the shop.")
    slow_print("What would you do next?")
    slow_print("""
    1. Go back to village entrance
    2. Enter the shop
    """)
    player_choice = valid_input("<Please enter the number of your choice.>",
                                ["1", "2"], name_holder[1], False)

    if player_choice == "1":
        village(counter, name_holder, player_attr, items)
    else:
        shop(counter, name_holder, player_attr, items)


def shop(counter, name_holder, player_attr, items):
    if name_holder[1] != 2:
        slow_print("Within a few minutes, you have reach the shop.")
    else:
        slow_print("in a blink of an eye, you have teleported yourself "
                   "inside the shop.")

    if "Q1" in items:
        if "copper" in items and "iron" in items and "silver" in items:
            if "weapon1" in items:
                items.remove("weapon1")
                items.append("weapon2")
                slow_print('"I have upgrade your "Wooden Sword" to "Metal '
                           'Sword"!"')
                slow_print('You received the "Metal Sword".')
            if "shield1" in items:
                items.remove("shield1")
                items.append("shield2")
                slow_print('"I have upgrade your "Wooden Shield" to "Metal '
                           'Shield"!"')
                slow_print('You received the "Metal Shield".')
            items.remove("copper")
            items.remove("iron")
            items.remove("silver")
            items.append("Q3")
        elif ("copper" in items and ("iron" in items or "silver" in items) and
                "Q2" in items):
            if "weapon1" in items:
                items.remove("weapon1")
                items.append("weapon2")
                slow_print('"I have upgrade your "Wooden Sword" to "Metal '
                           'Sword"!"')
                slow_print('You received the "Metal Sword".')
            elif "shield1" in items:
                items.remove("shield1")
                items.append("shield2")
                slow_print('"I have upgrade your "Wooden Shield" to "Metal '
                           'Shield"!"')
                slow_print('You received the "Metal Shield".')
            items.remove("copper")
            items.append("Q4")
            if "iron" in items:
                items.remove("iron")
            if "silver" in items:
                items.remove("silver")
        elif "leaf" in items and "root" in items and "flower" in items:
            items.append("poison")
            items.remove("leaf")
            items.remove("flower")
            slow_print('"You have brought me the ingredients! The poison '
                       'will be ready in no time!"')
            slow_print('You received the "Permanent Lethal Poison".')

    if "Q3" in items:
        swrd_up = True
        shld_up = True
    elif "weapon2" in items:
        swrd_up = True
        shld_up = False
    elif "shield2" in items:
        swrd_up = False
        shld_up = True
    else:
        swrd_up = False
        shld_up = False

    shopping(name_holder, player_attr, items, swrd_up, shld_up)

    if "Q1" not in items:
        if name_holder[1] == 1:
            if "weapon1" in items or "shield1" in items:
                slow_print('"Wait a second! If you can find me some ores, I '
                           'can upgrade your sword and shield to a more '
                           'powerful version."')
                slow_print('The shopkeeper told you to find "Copper", '
                           '"Iron", and "Silver" ore if you wish to '
                           'upgrade your weapon.')
                slow_print('"Two ores are require for one item and three '
                           'is enough for both!"')
                slow_print("He has no idea where these ores could be found, "
                           "but he suggest that some villagers might know.")
        elif name_holder[1] == 2:
            if "staff" in items:
                slow_print('"Wait a second! I heard some rumours that you '
                           'might interested since you are a Magician."')
                slow_print("The shopkeeper said there are sacred magical "
                           "items that hold unbelievable power.")
                slow_print('He not sure where are these items but he '
                           'certain it is related to "Dragonfly Bone" and '
                           '"Moon Leaf".')
                slow_print("He also suggest that some villagers might have "
                           "some clues.")
        else:
            if "dagger1" in items:
                slow_print('"Wait!", the shopkeeper stopped you.')
                slow_print('He told you that poison work well with the '
                           'dagger and he can made you a "Permanent Lethal '
                           'Poison".')
                slow_print('All he needs is some "Poison Leaf", "Spider '
                           'Root", and "Snake Flower" which is hard to find '
                           'nowadays.')
                slow_print("He suggested that you might get some "
                           "intelligence from the villagers.")
        items.append("Q1")

    slow_print("What would you do next?")
    slow_print("""
    1. Go back to village entrance
    2. Talk to the villagers
    """)
    player_choice = valid_input("<Please enter the number of your choice.>",
                                ["1", "2"], name_holder[1], False)

    if player_choice == "1":
        village(counter, name_holder, player_attr, items)
    else:
        vill_tlk(counter, name_holder, player_attr, items)


def shopping(name_holder, player_attr, items, swrd_up, shld_up):
    slow_print(f'"Welcome to my shop, {name_holder[0]}! Do you want something '
               'from my shop?", said the shopkeeper.')
    slow_print(f"You have {items[0]} gold")
    n = int((100 - player_attr[0]) / 5) + 1

    if swrd_up is False and shld_up is False:
        slow_print("""
        1. Wooden Sword     [Warrior]            200 gold
        2. Wooden Shield    [Warrior]            150 gold
        3. Wooden Staff     [Magician]            50 gold
        4. Wooden Dagger    [Others]             150 gold
        """)
    elif swrd_up is True and shld_up is False:
        slow_print("""
        1. Metal Sword      [Warrior]            200 gold
        2. Wooden Shield    [Warrior]            150 gold
        3. Wooden Staff     [Magician]            50 gold
        4. Wooden Dagger    [Others]             150 gold
        """)
    elif swrd_up is False and shld_up is True:
        slow_print("""
        1. Wooden Sword     [Warrior]            200 gold
        2. Metal Shield     [Warrior]            150 gold
        3. Wooden Staff     [Magician]            50 gold
        4. Wooden Dagger    [Others]             150 gold
        """)
    else:
        slow_print("""
        1. Metal Sword      [Warrior]            200 gold
        2. Metal Shield     [Warrior]            150 gold
        3. Wooden Staff     [Magician]            50 gold
        4. Wooden Dagger    [Others]             150 gold
        """)
    print(f"5. Medical Treatment                {n} gold")
    print("6. Exit\n")

    player_choice = valid_input("<Please enter the number of your choice.>",
                                ["1", "2", "3", "4", "5", "6"], name_holder[1],
                                False)

    if player_choice == "1":
        if ("weapon1" not in items and "weapon2" not in items and "weapon3" not
                in items):
            if items[0] >= 200:
                items[0] -= 200
                if swrd_up:
                    items.append("weapon2")
                    slow_print('You received "Metal Sword".')
                else:
                    items.append("weapon1")
                    slow_print('You received "Wooden Sword".')
            else:
                slow_print("You do not have enough gold.")
        else:
            slow_print("You already have an equivalent or better sword!")
        shopping(name_holder, player_attr, items, swrd_up, shld_up)
    elif player_choice == "2":
        if ("shield1" not in items and "shield2" not in items and "shield3" not
                in items):
            if items[0] >= 150:
                items[0] -= 150
                if shld_up:
                    items.append("shield2")
                    slow_print('You received "Metal Shield".')
                else:
                    items.append("shield1")
                    slow_print('You received "Wooden Shield".')
            else:
                slow_print("You do not have enough gold.")
        else:
            slow_print("You already have an equivalent or better shield!")
        shopping(name_holder, player_attr, items, swrd_up, shld_up)
    elif player_choice == "3":
        if "staff" not in items:
            if items[0] >= 50:
                items[0] -= 50
                items.append("staff")
            else:
                slow_print("You do not have enough gold.")
        else:
            slow_print("You already have a staff!")
        shopping(name_holder, player_attr, items, swrd_up, shld_up)
    elif player_choice == "4":
        if "dagger1" not in items and "dagger2" not in items:
            if items[0] >= 150:
                items[0] -= 150
                items.append("dagger1")
            else:
                slow_print("You do not have enough gold.")
        else:
            slow_print("You already have an equivalent or better dagger!")
        shopping(name_holder, player_attr, items, swrd_up, shld_up)
    elif player_choice == "5":
        if items[0] >= n:
            if player_attr[0] == 100:
                slow_print("You look good in condition! You do not require "
                           "medical attention for now!")
            else:
                items[0] -= n
                player_attr[0] = 100
                slow_print("You are healed!")
                print(f"Your Hp: {player_attr[0]}\n")
        else:
            slow_print("You do not have enough gold.")
        shopping(name_holder, player_attr, items, swrd_up, shld_up)


def lake(counter, name_holder, player_attr, items):
    if name_holder[1] != 2:
        slow_print("Within an hours, you have arrived the Lake.")
    else:
        slow_print("In a split second, you have teleported yourself to the "
                   "Lake.")

    enemy_reset(counter)

    slow_print("A beautiful environment with magical lake ......")

    if name_holder[1] == 1:
        if "Q2" in items and ("copper" not in items and "iron" not in items and
                              "silver" not in items) and counter[0] % 3 == 0:
            slow_print("You saw a Goddess walk toward you from the centre of "
                       "lake.")
            slow_print('"Young warrior, you have a kind heart."')
            slow_print('"The young lady you met before is actually my '
                       'disguise."')
            slow_print('"i admire your noble act and so you have passed my '
                       'trial."')
            slow_print('"Here is a little gift from me."')

            while "Q2" in items:
                if "weapon1" in items:
                    items.append("weapon3")
                    items.remove("Q2")
                    items.remove("weapon1")
                    slow_print('Your "Wooden Sword" has turned into "Divine '
                               'Sword"!')
                elif "shield1" in items:
                    items.append("shield3")
                    items.remove("Q2")
                    items.remove("shield1")
                    slow_print('Your "Wooden Shield" has turned into "Divine '
                               'Shield"!')
                if "Q5" not in items:
                    items.append("Q5")
            slow_print("The goddess disappeared in front of you...")

        if ("copper" in items and "iron" in items and "silver" not in items and
                "Q2" not in items and counter[0] % 3 == 0):
            slow_print('You found a "silver" ore at lakeside.')
            items.append("silver")
            slow_print("Suddenly a young lady called you, and begging you to "
                       "give some of the ores to her.")
            slow_print("After a short conversation, you know the lady "
                       "desperately needs the ores to pay levy to Dr. L.")
            slow_print("You want to help the lady but you know it will be "
                       "difficult to defeat Dr. L without good weapon.")

            slow_print("What would you do?")
            slow_print("""
            1. Give all the ores to the lady
            2. Give 2 ores to the lady
            3. Give only 1 ore to the lady
            4. Save all the ores to upgrade your equipment
            """)
            player_choice = valid_input("<Please enter the number of your "
                                        "choice.>", ["1", "2", "3", "4"],
                                        name_holder[1], False)

            if player_choice == "1" or player_choice == "2":
                items.append("Q2")
                items.append("Q2")
                items.remove("silver")
                items.remove("iron")
                items.remove("copper")
            elif player_choice == "3":
                items.append("Q2")
                items.remove("silver")

    elif name_holder[1] == 2:
        if "leaf" in items and "bone" in items and counter[0] % 3 == 0:
            slow_print("You suddenly feels a powerful energy surging out "
                       "from the lake!")
            slow_print("You thought this this is the best time to perform "
                       "a transformation spell to create a powerful magical "
                       "relic by channelling the lake energy.")
            slow_print("The Goddess of Lake saw your talent and decide to "
                       "help you to finish the ritual.")
            slow_print('By combining magics, you all successfully created '
                       'the "True Eyes Gem" that review only the True!')
            items.append("gem")
            items.remove("leaf")
            items.remove("bone")
            slow_print("You thanked the Goddess.")
            slow_print("Before she leave, she told you that you might found "
                       "another powerful sacred relic at cave behind the "
                       "mountain if you are blessed.")

    elif name_holder[1] == 3:
        if "poison" not in items and counter[0] % 3 == 0:
            slow_print("You heard a soft voice calling you.")
            slow_print('"Go to the forest now! And you shall find what you '
                       'seek ..."')
            slow_print("You look around but saw no one in ten miles...")
            slow_print("You are wondering should you give it a try. But "
                       "hesitated.")
            slow_print("Well, you are not the type that will follow order....")

    slow_print("What would you do?")
    slow_print("""
    1. Go to the village
    2. Go inside the forest
    3. Go to the mountain
    """)
    player_choice = valid_input("<Please enter the number of your choice.>",
                                ["1", "2", "3"], name_holder[1], False)

    if player_choice == "1":
        counter[0] += 1
        village(counter, name_holder, player_attr, items)
    elif player_choice == "2":
        counter[0] += 1
        forest(counter, name_holder, player_attr, items)
    else:
        counter[0] += 1
        mountain(counter, name_holder, player_attr, items)


def forest(counter, name_holder, player_attr, items):
    if name_holder[1] != 2:
        slow_print("Within an hours, you are in the forest.")
    else:
        slow_print("In a split second, you have teleported yourself to the "
                   "forest.")

    slow_print("A thick forest full of living organisms and species, also...")
    slow_print("Dangerous...")

    enemy_reset(counter)

    if counter[2]:
        creature_attr = [60, 9, 3]  # hp,atk,def
        encounter(name_holder, player_attr, creature_attr, items, False)
        counter[2] = False

    if player_attr[0] > 0:
        if name_holder[1] == 2:
            if "Q1" in items and "gem" not in items and "leaf" not in items:
                n = random.randint(1, 6)
                if n == 1 or n == 6:
                    slow_print('You found the "Moon Leaf"! What a lucky '
                               'person you are!')
                    items.append("leaf")
                else:
                    slow_print("You did not found anything.")
                    slow_print("You are out of luck...")
        elif name_holder[1] == 3:
            if ("Q1" in items and "poison" not in items and
                    ("leaf" not in items or "root" not in items or "flower"
                     not in items)):
                if counter[0] % 3 == 1:
                    if "leaf" not in items:
                        slow_print('You found the "Poison Leaf"!')
                        items.append("leaf")
                    elif "root" not in items:
                        slow_print('You again found the "Spider Root"!')
                        items.append("root")
                    else:
                        slow_print('You found the last ingredients - "Snake '
                                   'Flower"!')
                        items.append("flower")

                    slow_print("You pick it up carefully to avoid poisoning "
                               "yourself.")

        slow_print("What would you do next?")
        slow_print("""
        1. Go to the village
        2. Go to the lakeside nearby the village
        3. Go to the mountain
        """)
        player_choice = valid_input("<Please enter the number of your "
                                    "choice.>", ["1", "2", "3"],
                                    name_holder[1], False)

        if player_choice == "1":
            counter[0] += 1
            village(counter, name_holder, player_attr, items)
        elif player_choice == "2":
            counter[0] += 1
            lake(counter, name_holder, player_attr, items)
        else:
            counter[0] += 1
            mountain(counter, name_holder, player_attr, items)


def mountain(counter, name_holder, player_attr, items):
    if name_holder[1] != 2:
        slow_print("Within an hours, you found yourself located in the "
                   "mountain.")
    else:
        slow_print("In a split second, you have teleported yourself to the "
                   "mountain.")

    enemy_reset(counter)

    slow_print("It is cold and chill in here ...")
    slow_print("You just saw a bunch of rocks and a few trees.")

    if (name_holder[1] == 1 and "Q1" in items and "iron" not in items and
            "Q2" not in items and "Q3" not in items and "Q4" not in items
            and "Q5" not in items):
        slow_print('You found a "Iron" ores!')
        items.append("iron")

    slow_print("What would you do next?")
    slow_print("""
    1. Go to the lakeside nearby the village
    2. Go inside the forest
    3. Go inside the cave behind the mountain
    4. Go to the castle
    """)
    player_choice = valid_input("<Please enter the number of your choice.>",
                                ["1", "2", "3", "4"], name_holder[1], False)

    if player_choice == "1":
        counter[0] += 1
        lake(counter, name_holder, player_attr, items)
    elif player_choice == "2":
        counter[0] += 1
        forest(counter, name_holder, player_attr, items)
    elif player_choice == "3":
        counter[0] += 1
        cave(counter, name_holder, player_attr, items)
    else:
        counter[0] += 1
        castle(counter, name_holder, player_attr, items)


def cave(counter, name_holder, player_attr, items):
    if name_holder[1] != 2:
        slow_print("Within an hours, you found yourself located in the "
                   "cave.")
    else:
        slow_print("In a split second, you have teleported yourself to the "
                   "cave.")

    enemy_reset(counter)

    if counter[3]:
        creature_attr = [60, 11, 3]  # hp,atk,def
        encounter(name_holder, player_attr, creature_attr, items, False)
        counter[3] = False

    if player_attr[0] > 0:
        slow_print("It is a big cave!")

        if name_holder[1] == 2:
            if "gem" in items and "stone" not in items:
                n = random.randint(1, 6)
                m = random.randint(1, 6)
                k = random.randint(1, 6)

                if n + m + k >= 14 and random.randint(0, 1) == 1:
                    slow_print('Your "True Eyes Gem" shine brightly.')
                    slow_print('You saw a small stone shine as bright as the '
                               'gem.')
                    slow_print('You knew this is the sacred relic you are '
                               'looking!')
                    slow_print('A "Lucky Sorcerer Stone"!')
                    items.append("stone")

            if "gem" not in items and "bone" not in items:
                if random.randint(1, 6) == 5:
                    items.append("bone")
                    slow_print('Your found the rare "Dragonfly Bone"!')

        if random.randint(1, 3) == 1:
            n = random.randint(2, 5)
            slow_print(f"You found {n} gold!")
            slow_print(f"You now have {items[0]} gold!")

        slow_print("There is nothing more in the cave and you decided to "
                   "head back to the mountain.")
        counter[0] += 1
        mountain(counter, name_holder, player_attr, items)


def castle(counter, name_holder, player_attr, items):
    if name_holder[1] != 2:
        slow_print("Within an hours, you found yourself reached the castle.")
    else:
        slow_print("In a split second, you have teleported yourself to the "
                   "castle.")

    slow_print("A creature stand in front of you and start attacking!")
    creature_attr = [80, 12, 5]  # hp,atk,def
    fight(name_holder, player_attr, creature_attr, items, creature_attr[0],
          False)

    if player_attr[0] > 0:
        slow_print("A giant evil creature arrived!!!")
        slow_print('You know it must be "Dr. L" ...')
        slow_print("It quickly attack you with a bolt of fire!!!")
        boss_attr = [200, 35, 40]  # hp,atk,def
        fight(name_holder, player_attr, boss_attr, items, boss_attr[0], True)


def G_Over(name_holder, player_attr):
    if player_attr[0] > 0:
        time.sleep(1)
        slow_print("You have defeated Dr.L and saved the unknown world!")
    else:
        slow_print("You fight well, but you are still no match to Dr. L and "
                   "its creatures.")

    player_choice = valid_input2("<Do you want replay the game? (y/n)>",
                                 name_holder[1], True)

    if player_choice == "y":
        gameplay()
    else:
        print("Game Over!")
        print("Thank you for playing. Bye!")


def gameplay():
    name_holder = []
    items = [400]  # gold
    player_attr = [100, 5, 2]  # hp,atk,def
    counter = [1, True, True, True]  # Move,[village,forest,cave] enemy show up

    intro(name_holder)
    role_select(name_holder)
    village(counter, name_holder, player_attr, items)
    G_Over(name_holder, player_attr)


gameplay()
