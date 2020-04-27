import tcod

from game_states import GameStates
from renderer.render_functions import RenderOrder

def kill_player(player):
    player.char = '%'
    player.color = tcod.dark_red

    return 'You have died.', GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = F"{monster.name.capitalize()} is dead!"
    
    monster.name = F"remains of {monster.name}"
    monster.char = '%'
    monster.color = tcod.dark_red
    monster.blocks = False
    monster.render_order = RenderOrder.CORPSE
    monster._Fighter = None
    monster._Ai = None
    
    return death_message