import tcod
from dice import roll_dice

from random import randint
from game_messages import Message
from renderer.render_functions import draw_animation


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.__Fighter.hp == entity.__Fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health', tcod.yellow)})
    else:
        entity.__Fighter.heal(amount)
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

    chance = randint(1,9)
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
        talk = "laughs softly."
    elif chance == 9:
        talk = "tells you she could really have a walk, but is trapped in this talisman."

    results.append({'used': True,
                    'message': Message(F'You look at the talisman. The devil of the talisman {talk}', tcod.lighter_purple)})
    return results

def cast_spell(*args, **kwargs):
    results = []
    camera = kwargs.get('camera')
    screen_width = kwargs.get('screen_width')
    screen_height = kwargs.get('screen_height')
    fov_map = kwargs.get('fov_map')

    caster = args[0]
    entities = kwargs.get('entities')
    damage = roll_dice(kwargs.get('damage'))
    maximum_range = kwargs.get('maximum_range')

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity._Fighter and entity != caster and fov_map.fov[entity.y, entity.x]:
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        draw_animation(0, camera, screen_width, screen_height, target.x, target.y, 'flash')
        tcod.console_blit(0, 0, 0, screen_width, screen_height, 0, 0, 0)
        tcod.console_flush(keep_aspect=True)

        results.append({'consumed': True, 'target': target,
                        'message': Message(F'A crackling stream of energy hits {target.name} for {damage} hit points.')})
        results.extend(target._Fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemy is close enough to strike.', tcod.red)})

    return results

def cast_fireball(*args, **kwargs):
    results = []
    camera = kwargs.get('camera')
    screen_width = kwargs.get('screen_width')
    screen_height = kwargs.get('screen_height')
    fov_map = kwargs.get('fov_map')

    entities = kwargs.get('entities')
    damage_dice = kwargs.get('damage')
    radius = kwargs.get('radius')
    r = int((radius-1) / 2)
    target_x = kwargs.get('target_x') - camera.x
    target_y = kwargs.get('target_y') - camera.y

    if not fov_map.fov[target_y, target_x]:
        results.append({'consumed': False,
                        'message': Message('You cannot target a tile outside your field of view.', tcod.yellow)})
        return results

    for x in range(target_x - r, target_x + r + 1):
        for y in range(target_y - r, target_y + r + 1):
            draw_animation(0, camera, screen_width, screen_height, x,y, 'explosion')

    tcod.console_blit(0, 0, 0, screen_width, screen_height, 0, 0, 0)
    tcod.console_flush(keep_aspect=True)
    results.append({'consumed': True,
                    'message': Message(F'The flaming sphere explodes!', tcod.orange)})
    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity._Fighter:
            damage = roll_dice(damage_dice)
            results.append({'message': Message(F'{entity.name} gets blasted for {damage} hit points.', tcod.orange)})
            results.extend(entity._Fighter.take_damage(damage))
    return results