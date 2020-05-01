import tcod

from game_messages import Message
from random import randint

class Fighter:
    def __init__(self, hp, defense, power, sanity=0):
        """
        체력, 방어력, 공격력
        """
        self.max_hp = hp
        self.hp = hp
        self.max_sanity = sanity
        self.cap_sanity = sanity
        self.sanity = sanity

        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        results = []
        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner})
        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def heal_sanity(self, amount):
        self.sanity += amount

        if self.sanity > self.cap_sanity:
            self.sanity = self.cap_sanity

    def heal_sanity_capacity(self, amount, also_heal_sanity=True):
        self.cap_sanity += amount

        if self.cap_sanity > self.max_sanity:
            self.cap_sanity = self.max_sanity

        if also_heal_sanity:
            self.heal_sanity(amount)

    def attack(self, target):
        results = []
        damage = randint(0,self.power) - randint(0,target._Fighter.defense)

        entity_name = self.owner.name.capitalize()
        if damage > 0:
            results.append({'message': Message(f'{entity_name} hit {target.name} for {damage} hit points.',
                           tcod.white)})
            results.extend(target._Fighter.take_damage(damage))
        else:
            results.append({'message': Message(f'{entity_name} hit {target.name} but does no damage.',tcod.white)})
        return results