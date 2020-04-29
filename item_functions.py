import tcod

from random import randint
from game_messages import Message


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity._Fighter.hp == entity._Fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health', tcod.yellow)})
    else:
        entity._Fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', tcod.green)})

    return results

def read(*args, **kwargs):
    entity = args[0]
    about = kwargs.get('about')
    #content = kwargs.get('content')

    results = []

    results.append({'used': True,
                    'message': Message(F'You open the book and read... This is a book {about}.', tcod.white)})

    return results

def talisman(*args, **kwargs):
    results = []

    chance = randint(1,8)
    if chance == 1:
        talk = "askes you how are things going."
    elif chance == 2:
        talk = "tells you that she and Mary knew each other."
    elif chance == 3:
        talk = "says she think that you should hurry."
    elif chance == 4:
        talk = "tells you that death is nothing compared to the meaningless of life."
    elif chance == 5:
        talk = "smiles breifly."
    elif chance == 6:
        talk = "worries about Mary."
    elif chance == 7:
        talk = "assures you how time travel is completely possible even within the theory of relativity."
    elif chance == 8:
        talk = "wonders why you're talking with her when there's little time left."

    results.append({'used': True,
                    'message': Message(F'You look at the talisman. The devil of the talisman {talk}', tcod.lighter_purple)})
    return results