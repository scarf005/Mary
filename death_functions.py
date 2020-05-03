import tcod

from batchim import Batchim

from game_states import GameStates
from renderer.render_functions import RenderOrder
from game_messages import Message

from yaml_functions import read_yaml, cout

SYS_LOG = read_yaml("system_log.yaml")

def kill_player(player):
    player.char = '%'
    player.color = tcod.dark_red

    return Message('You have died.', tcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = Message(cout(SYS_LOG['death_log'],monster.name.capitalize()), tcod.orange)
    monster.name = cout(SYS_LOG['dead_entity'],Batchim(monster.name.capitalize(),'(이','('))
    monster.char = '%'
    monster.color = tcod.dark_red
    monster.blocks = False
    monster.render_order = RenderOrder.CORPSE
    monster._Fighter = None
    monster._Ai = None

    return death_message