import tcod
from init_constants import *


def menu(root, con, header, options, line_up=True):
    """
    a,b,c 등으로 정렬해줌
    """

    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate root height for the header (after auto-wrap) and one line per option
    header_height = tcod.console_get_height_rect(con, 0, 0, MESSAGE_WIDTH, SCREEN_HEIGHT, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = tcod.Console(MESSAGE_WIDTH, height)

    # print the header, with auto-wrap
    window.print_box(0, 0, MESSAGE_WIDTH, height, header, alignment=tcod.LEFT)

    # print all the options
    y = header_height
    letter_index = ord('a')

    for option_text in options:
        if line_up:
            text = F"({chr(letter_index)}) {option_text}"
        else:
            text = option_text
        window.print(0, y, text, alignment=tcod.LEFT, fg=tcod.white)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(SCREEN_WIDTH / 2 - MESSAGE_WIDTH / 2)
    y = int(MAP_HEIGHT / 2 - height / 2)
    window.blit(root, x, y, 0, 0, MESSAGE_WIDTH, height, fg_alpha=1.0, bg_alpha=0.7)

def inventory_menu(root, con, header, inventory, line_up):
    # show a menu with each item of the inventory as an option
    if len(inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for item in inventory.items:
            options.append(item.name if item._Item.quantity == 1 else F"{item.name} x {item._Item.quantity}")

    menu(root, con, header, options, line_up)

def character_screen(root, con, player):
    window = tcod.Console(MESSAGE_HEIGHT, SCREEN_HEIGHT)