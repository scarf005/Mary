import tcod

class BasicAi:
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
                results.extend(self.attack(monster, target))

        return results

    def attack(self, monster, target):
        return monster._Fighter.attack(target)

class MaryAi(BasicAi):
    def attack_other(self, target):
        pass

    def take_turn(self, target, fov_map, game_map, entities):

        results = []
        mary = self.owner

        if fov_map.fov[mary.y, mary.x]:
            if mary.distance_to(target)  >= 2:
                mary.move_astar(target, entities, game_map)

            elif target._Fighter.hp > 0:
                results.append({'game_won': True})

        return results