import tcod
import copy
import numpy as np
import time

if not __name__ == "__main__":
    from .render_functions import draw_background
    from init_constants import *

#화면 표시
def refresh_console(root, animation_console, context, fg_alpha=0, bg_alpha=1, wait=0):
    animation_console.blit(root, fg_alpha=fg_alpha, bg_alpha=bg_alpha, key_color=(0,0,0))
    context.present(root, keep_aspect=True, align=(0.5,0.5))
    animation_console.clear()
    time.sleep(wait)

#한칸짜리 그림 그림
def draw_animation(con, camera, x, y, string, **kwargs):
    """
    print(x: int, y: int, string: str,
    fg: Optional[Tuple[int, int, int]] = None,
    bg: Optional[Tuple[int, int, int]] = None,
    bg_blend: int = 1,
    alignment: int = 0)
    """
    MapX = x + camera.x + CENTER_X
    MapY = y + camera.y + CENTER_Y
    if string == "":
        tcod.console_set_char_background(con, MapX, MapY, flag=tcod.BKGND_SET,**kwargs)
    else:
        con.print(MapX, MapY, string, **kwargs)

# 글자 복구
def clear_animation(con, camera, x, y, color):
    MapX = x + camera.x + CENTER_X
    MapY = y + camera.y + CENTER_Y

    #tcod.console_put_char(con, MapX, MapY, char, tcod.BKGND_NONE)
    #draw_background(con, MapX, MapY, color, 30)

# 선 그리기
def get_line(path_map, x1,y1, x2,y2):
    astar = tcod.path.AStar(path_map)
    result = astar.get_path(y1,x1, y2,x2)
    return result

if __name__ == "__main__":
    gmap = np.ones((4,10), dtype='uint8')
    print(gmap)
    print(get_line(gmap, 0,0, 9,3))

