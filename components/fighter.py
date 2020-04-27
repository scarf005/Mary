class Fighter:
    def __init__(self, hp, defense, power):
        """
        체력, 방어력, 공격력
        """
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power