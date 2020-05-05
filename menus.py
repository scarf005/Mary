import tcod


def menu(root, con, header, options, width, screen_width, screen_height, map_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate root height for the header (after auto-wrap) and one line per option
    header_height = tcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = tcod.Console(width, height)

    # print the header, with auto-wrap
    tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = F"({chr(letter_index)}) {option_text}"
        window.print(0, y, text, alignment=tcod.LEFT, fg=tcod.white)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(map_height / 2 - height / 2)
    window.blit(root, x, y, 0, 0, width, height, fg_alpha=1.0, bg_alpha=0.7)

def inventory_menu(root, con, header, inventory, inventory_width, screen_width, screen_height, map_height):
    # show a menu with each item of the inventory as an option
    if len(inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for item in inventory.items:
            options.append(item.name if item._Item.quantity == 1 else F"{item.name} x {item._Item.quantity}")

    menu(root, con, header, options, inventory_width, screen_width, screen_height, map_height)