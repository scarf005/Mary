import tcod
import sys
sys.path.append('C:\\msys64\\home\\Pig\\Mary')
from entity import Entity

from equipment_slots import EquipmentSlots

class Equippable:
    def __init__(self, slot, **kwargs):
        """
        장비할 수 있는 물건들. 무기부터 장신구까지.
        """
        self.slot = slot

        # 기타 속성들
        attributes_list = {'attack_power':0, 'attack_type':None,
                            'armour_class':0, 'sanity_resistance':0,
                            'max_hp':0, 'regen_hp':0,
                            'curse':None}

        total_list = {**attributes_list}
        for key,value in total_list.items():
            if key in kwargs.keys():
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, value)

if __name__ == "__main__":
    equip_comp = Equippable(EquipmentSlots.SCARF, sanity_resistance=20)
    green_scarf = Entity(0,0,'^',tcod.green,"green scarf", _Equippable=equip_comp)
    print(green_scarf.total_sanity_resist)
