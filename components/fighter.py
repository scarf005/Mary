import tcod

from game_messages import Message
from random import randint

class Fighter:
    def __init__(self, hp, defense, power):
        """
        체력, 방어력, 공격력
        """
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        results = []
        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner})
        return results

    def attack(self, target):
        results = []
        damage = randint(0,self.power) - randint(0,target._Fighter.defense)

        entity_name = self.owner.name.capitalize()
        if damage > 0:
            results.append({'message': Message(F'{entity_name} attacks {target.name} for {damage} hit points.',
                           tcod.white)})
            results.extend(target._Fighter.take_damage(damage))
        else:
            results.append({'message': Message(F'{entity_name} attacks {target.name} but does no damage.',tcod.white)})
        return results