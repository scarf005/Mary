from random import randint

def random_choice_from_dict(choice_dict):
    def random_choice_index(chances):
        random_chance = randint(1, sum(chances))

        running_sum = 0
        choice = 0
        for w in chances:
            running_sum += w

            if random_chance <= running_sum:
                return choice
            choice += 1

    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]

if __name__ == '__main__':
    # DEMO
    item_chances = {'A': 70, 'B': 10, 'C': 10, 'D': 10}
    for i in range (100):
        item_choice = random_choice_from_dict(item_chances)
        print(item_choice)