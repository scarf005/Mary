import tcod
import math, time
from dice import roll_dice

from random import randint
from game_messages import Message
from renderer.render_functions import draw_animation

from yaml_functions import read_yaml, cout
from batchim import Batchim

SYS_LOG = read_yaml("system_log.yaml")
ITEM_LOG = read_yaml("item_log.yaml")

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')
    which_heal = kwargs.get('which')
    if not which_heal:
        which_heal = 'hp'

    results = []

    if which_heal == 'hp':
        if entity._Fighter.hp == entity._Fighter.max_hp:
            results.append({'consumed': False, 'message': Message(SYS_LOG['full_health'], tcod.yellow)})
        else:
            entity._Fighter.heal(amount)
            results.append({'consumed': True, 'message': Message(SYS_LOG['heal_health'], tcod.green)})

    elif which_heal == 'sanity':
        if entity._Fighter.sanity == entity._Fighter.cap_sanity:
            results.append({'consumed': False, 'message': Message(SYS_LOG['full_sanity'], tcod.yellow)})
        else:
            entity._Fighter.heal_sanity(amount)
            results.append({'consumed': True, 'message': Message(SYS_LOG['heal_sanity'], tcod.green)})

    return results

def read(*args, **kwargs):
    entity = args[0]
    about = kwargs.get('about')
    sanity = kwargs.get('sanity')
    content = kwargs.get('content')

    if content:
        snippet = f" This part says:{content(randint(0,len(content)-1))}"
    else:
        snippet = ""

    feeling = ""
    if sanity:
        entity._Fighter.heal_sanity(sanity)
        if sanity > 0:
            feeling = "This feels better."
        elif sanity == 0:
            feeling = ""
        elif sanity < 0:
            feeling = "This makes you feel worse."

    results = []

    results.append({'used': True,
                    'message': Message(F' {about}.{snippet}{feeling}',
                                       tcod.white)})

    return results

def talisman(*args, **kwargs):
    results = []
    talisman = read_yaml("artifacts.yaml")['talisman']
    log = talisman['quotes'][randint(0,len(talisman)-1)]

    results.append({'used': True,
                    'message': Message(cout(talisman,log),tcod.lighter_purple)})
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

        results.append({'consumed': True, 'target': target,
                        'message': Message(F'A crackling stream of energy hits {target.name} for {damage} hit points.')})
        results.extend(target._Fighter.take_damage(damage))
        time.sleep(0.1)
    else:
        results.append({'consumed': False, 'target': None, 'message': Message(SYS_LOG['no_close_enemy'], tcod.red)})

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
                        'message': Message(SYS_LOG['outside_fov'], tcod.yellow)})
        return results

    for x in range(target_x - r, target_x + r + 1):
        for y in range(target_y - r, target_y + r + 1):
            draw_animation(0, camera, screen_width, screen_height, x,y, 'explosion')

    tcod.console_blit(0, 0, 0, screen_width, screen_height, 0, 0, 0)
    results.append({'consumed': True,
                    'message': Message(F'The flaming sphere explodes!', tcod.orange)})
    time.sleep(0.1)
    for entity in entities:
        #print(F"{entity.name} {entity.distance(target_x, target_y)}")
        if entity.distance(target_x, target_y) <= math.sqrt(2*(r**2)) and entity._Fighter:
            damage = roll_dice(damage_dice)
            results.append({'message': Message(F'{entity.name} is blasted for {damage} hit points.', tcod.orange)})
            results.extend(entity._Fighter.take_damage(damage))
    return results