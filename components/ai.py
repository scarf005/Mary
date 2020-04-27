import tcod

class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        """
        target: 목표 대상
        fov_map, game_map, entities: 계산용
        """
        results = []
        monster = self.owner
        
        if fov_map.fov[monster.y, monster.x]:
            if monster.distance_to(target)  >= 2:
                monster.move_astar(target, entities, game_map)

            elif target._Fighter.hp > 0:
                results.extend(monster._Fighter.attack(target))
        
        return results