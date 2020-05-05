class Equippable:
    def __init__(self, slot, **kwargs):
        """
        장비할 수 있는 물건들. 무기부터 장신구까지.
        """
        # 장비 위치
        self.slots_list = ['wielding', 'outfit', 'scarf', 'jewellery']
        self.slot = slot

        # 기타 속성들
        args_list = {}
        attributes_list = {'attack_power':0, 'attack_type':None,
                          'armour_class':0, 'sanity_resistance':None,
                          'max_hp':0, 'regen_hp':0,
                          'curse':None}

        total_list = {**args_list, **attributes_list}
        for key,value in total_list.items():
            if key in kwargs.keys():
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, value)

        print (self.__dict__)

    @property
    def total_sanity_resist(self):
        R = 0
        """
        for equipment in self.slots_list:
            print("loop")
            equip = getattr(self, equipment, None)
            print(equip)
            if equip:
                print(equip)
        """
        return R


if __name__ == "__main__":
    #green_scarf = Equippable('scarf')
    #print(green_scarf.total_sanity_resist())
