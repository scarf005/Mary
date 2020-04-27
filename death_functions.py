import tcod

from game_states import GameStates
from renderer.render_functions import RenderOrder
from game_messages import Message

def kill_player(player):
    player.char = '%'
    player.color = tcod.dark_red

    return Message('You have died.', tcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = Message(F"{monster.name.capitalize()} is dead!", tcod.orange)
    
    monster.name = F"what is left of {monster.name}"
    monster.char = '%'
    monster.color = tcod.dark_red
    monster.blocks = False
    monster.render_order = RenderOrder.CORPSE
    monster._Fighter = None
    monster._Ai = None
    
    return death_message