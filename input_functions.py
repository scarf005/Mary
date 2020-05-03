import tcod
import tcod.event
from game_states import GameStates

LOG = False
LOG2 = False

MOVE_KEYS = {  # key_symbol: (x, y)
    # Arrow keys.
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),
    #tcod.event.K_PERIOD: (0, 0),
    # Numpad keys.
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_5: (0, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),
    tcod.event.K_CLEAR: (0, 0),  # Numpad `clear` key.
    # Vi Keys.
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1),
}

PLAYER_INPUT = {
    'q':'toggle_light',
    ',':'pickup',
    '.':'rest',
    'i':'show_inventory',
    'd':'drop_inventory',
    #'1':'toggle_wall',
    #'2':'create_luminary'
}

INVENTORY_INPUT = 'INVENTORY'

class State(tcod.event.EventDispatch[None]):
    """A state-based superclass that converts `events` into `commands`.

    The configuration used to convert events to commands are hard-coded
    in this example, but could be modified to be user controlled.

    Subclasses will override the `cmd_*` methods with their own
    functionality.  There could be a subclass for every individual state
    of your game.
    """
    def __init__(self, available):
        self.result = {}
        self.key_list = available

    def ev_quit(self, event: tcod.event.Quit) -> None:
        """The window close button was clicked or Alt+F$ was pressed."""
        if LOG: print(event)
        self.cmd_quit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if LOG2: print("A key was pressed.")
        if LOG: print(event)
        if event.sym in MOVE_KEYS:
            # Send movement keys to the cmd_move method with parameters.
            self.cmd_move(*MOVE_KEYS[event.sym])
        elif event.sym == tcod.event.K_ESCAPE:
            self.cmd_escape()
        elif self.key_list == "INVENTORY":
            index = event.sym - ord('a')
            if index >= 0:
                self.result.update({'inventory_index': index})


    def ev_textinput(self, event: tcod.event.TextInput) -> None:
        if event.text in self.key_list:
            self.result.update({self.key_list.get(event.text): True})

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> None:
        if LOG2: print("The window was clicked.")
        if LOG: print(event)
        x,y = (event.tile.x, event.tile.y)
        if event.button == 1:
            self.result.update({'left_click': (x, y)})
        elif event.button == 3:
            self.result.update({'right_click': (x, y)})

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if LOG2: print("The mouse has moved within the window.")
        if LOG: print(event)
        (x,y) = (event.tile.x, event.tile.y)
        self.result.update( {'mouse_pos': (x,y)})

    def cmd_move(self, x: int, y: int) -> None:
        if LOG2: print("Intent to move: `x` and `y` is the direction, both may be 0.")
        self.result.update( {'move': (x, y)})

    def cmd_escape(self) -> None:
        if LOG2: print("Intent to exit this state.")
        if LOG: print("Command escape.")
        self.result.update( {'exit': True})

    def cmd_quit(self) -> None:
        if LOG2: print("Intent to exit the game.")
        if LOG: print("Command quit.")
        self.result.update( {'quit': True})


def handle_input_per_state(context, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_input(context, PLAYER_INPUT)
    elif game_state == GameStates.PLAYER_DEAD:
        return #handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return #handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_input(context, INVENTORY_INPUT)

    return {}

def handle_input(context, available_key_list):
    state = State(available_key_list)
    for event in tcod.event.wait():
        context.convert_event(event)
        state.dispatch(event)
        print(state.result)

        if not state.result == None:
            return state.result

        if event.type == "QUIT":
            raise SystemExit()
        if event.type == "WINDOWRESIZED":
                console = tcod.Console(*context.recommended_console_size())

    return {}

"""
#  # Set tile coordinates for an event.

if event.type == "WINDOWRESIZED":
    console = tcod.Console(*context.recommended_console_size())
if event.type == "TEXTINPUT":
    return event.text
"""