import tcod 

def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
    #fov 재계산 시만
    if fov_recompute:
        #지도에 있는 모든 타일을 그림
        for y in range(game_map.height):
            for x in range(game_map.width):
                #wall 불리언에 tile의 block_sight이 True인지 여부를 대입
                visible = fov_map.fov[y,x]
                wall = game_map.tiles[y,x].block_sight

                if visible:
                    if wall:
                        tcod.console_set_char_background(con, x, y, colors.get('light_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colors.get('light_ground'), tcod.BKGND_SET)
                    game_map.tiles[y,x].explored = True
                elif game_map.tiles[y,x].explored:
                    if wall:
                        tcod.console_set_char_background(con, x, y, colors.get('dark_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colors.get('dark_ground'), tcod.BKGND_SET)
                else:
                    pass
                    #draw_background(con,x,y,'pitch_black')


    #목록에 있는 모든 객체를 표시함.
    for entity in entities:
        draw_entity(con, entity, fov_map)

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    #목록에 있는 모든 객체를 제거함.
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map):
    #객체를 표시함.
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y):
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

def clear_entity(con, entity):
    #객체를 화면에서 지움
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)

def draw_background(con,x,y,colors,flag='BKGND_SET'):
    tcod.console_set_char_background(con, x, y, colors.get(colors), tcod.flag)