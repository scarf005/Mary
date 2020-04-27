import tcod

class BasicMonster:
    def take_turn(self, message, target, fov_map, game_map, entities):
        """
        message: 로그 띄우기
        target: 목표 대상
        fov_map, game_map, entities: 계산용
        """
        monster = self.owner
        if fov_map.fov[monster.y, monster.x]:
            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_map, entities)

            elif target._Fighter.hp > 0:
                message.log(F'The {monster.name} insults you! Your ego is damaged!')