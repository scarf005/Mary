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
        self.hp -= amount
        
    def attack(self, message, target):
        damage = self.power - target._Fighter.defense

        entity_name = self.owner.name.capitalize()
        if damage > 0:
            target._Fighter.take_damage(damage)
            message.log(F'{entity_name} attacks {target.name} for {damage} hit points.')
        else:
            message.log(F'{entity_name} attacks {target.name} but does no damage.')