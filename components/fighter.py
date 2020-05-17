import tcod

from game_messages import Message
from random import randint

from yaml_functions import read_yaml, cout
from batchim import 받침

SYS_LOG = read_yaml("system_log.yaml")

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

        self.base_defense = defense
        self.base_power = power
        #self.base_rsanity = 0

    def get_value(self, base, which):
        if self.owner and self.owner._Equipment:
            bonus = getattr(self.owner._Equipment, which)
        else:
            bonus = 0
        return getattr(self, base) + bonus

    @property
    def power(self):
        return self.get_value('base_power','total_attack_power')

    @property
    def defense(self):
        return self.get_value('base_defense','total_defense_power')


    def take_damage(self, amount, dmg_type='hp'):
        results = []
        if dmg_type == 'hp':
            self.hp -= amount

            if self.hp <= 0:
                results.append({'dead': self.owner})
        elif dmg_type == 'sanity':
            self.cap_sanity -= amount

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
            results.append({'message': Message(cout(SYS_LOG['fight_log'],
                                                    받침(entity_name,2),받침(target.name,1),
                                                    damage),tcod.white)})
            results.extend(target._Fighter.take_damage(damage))
            results.extend(target._Fighter.take_damage(int(damage/randint(1,damage)),dmg_type='sanity'))
        else:
            results.append({'message': Message(cout(SYS_LOG['fight_no_dmg_log'],
                                                    받침(entity_name),받침(target.name,1)),tcod.white)})
        return results
