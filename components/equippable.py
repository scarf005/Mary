class Equippable:
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        # 써도 사라지지 않는 물건들.
        self.slot = slot
        attribute_list = {'attack_power':0, 'attack_type':None,
                          'armour_class':0, 'resistance':None,
                          'max_hp':0, 'regen_hp':0,
                          'curse':None}