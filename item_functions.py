import tcod
import math, time
import numpy as np
from dice import roll_dice

from random import randint
from game_messages import Message
from renderer.animation_functions import refresh_console, draw_animation, get_line

from yaml_functions import read_yaml, cout
from batchim import 받침

from init_constants import CENTER_X, CENTER_Y, SCREEN_WIDTH, SCREEN_HEIGHT, colors

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

    root = kwargs.get('root')
    animation = kwargs.get('animation')
    context = kwargs.get('context')

    camera = kwargs.get('camera')
    screen_width = kwargs.get('screen_width')
    screen_height = kwargs.get('screen_height')

    fov_map = kwargs.get('fov_map')
    game_map = kwargs.get('game_map')

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
        path_map = np.ones((game_map.height,game_map.width),dtype='uint8')
        pos = get_line(path_map,caster.x,caster.y,target.x,target.y)

        chars = "!?#$%^&*\|;"
        flash = tuple(colors.get('flash'))

        for i in range(7):
            for n, position in enumerate(pos):
                if n == len(pos)-1:
                    draw_animation(root, camera, position[1], position[0], "", col=flash)
                else:
                    draw_animation(animation, camera, position[1], position[0],
                                string=chars[randint(0,len(chars)-1)], fg=tcod.white, bg=flash)

            refresh_console(root, animation, context, 1, 0.5, 0.03)

        results.append({'consumed': True, 'target': target,
                        'message': Message(cout(ITEM_LOG['magic_attack'],
                                                받침(ITEM_LOG['magic']['spell']['name']),
                                                ITEM_LOG['magic']['spell']['effect'],
                                                받침(target.name,1),
                                                damage), tcod.orange)
                                                })
        results.extend(target._Fighter.take_damage(damage))

    else:
        results.append({'consumed': False, 'target': None, 'message': Message(SYS_LOG['no_close_enemy'], tcod.red)})

    return results

def cast_fireball(*args, **kwargs):
    results = []

    animation = kwargs.get('animation')
    root = kwargs.get('root')
    context = kwargs.get('context')

    camera = kwargs.get('camera')
    fov_map = kwargs.get('fov_map')

    entities = kwargs.get('entities')
    damage_dice = kwargs.get('damage')
    radius = kwargs.get('radius')
    r = int((radius-1) / 2)
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    if not fov_map.fov[target_y, target_x]:
        results.append({'consumed': False,
                        'message': Message(SYS_LOG['outside_fov'], tcod.yellow)})
        return results

    ex = tuple(colors.get('explosion'))
    for x in range(target_x - r, target_x + r + 1):
        for y in range(target_y - r, target_y + r + 1):
            draw_animation(animation, camera, x,y, " ", bg=ex)

    refresh_console(root, animation, context, 0, 1 , 0.15)

    results.append({'consumed': True, 'animate': True,
                    'message': Message(ITEM_LOG['magic']['fireball']['describe'], tcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= math.sqrt(2*(r**2)) and entity._Fighter:
            damage = roll_dice(damage_dice)
            results.append({'message': Message(cout(ITEM_LOG['magic_attack'],
                                                받침(ITEM_LOG['magic']['fireball']['name']),
                                                ITEM_LOG['magic']['fireball']['effect'],
                                                받침(entity.name,1),
                                                damage), tcod.orange)})
            results.extend(entity._Fighter.take_damage(damage))
    return results