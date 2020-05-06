import tcod
import sys
sys.path.append('C:\\msys64\\home\\Pig\\Mary')

from entity import Entity

from .fighter import Fighter
from .inventory import Inventory
from enums.equipment_slots import EquipmentSlots
from .equipment import Equipment

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
    """
    적용 테스트
    """

    # 목도리 장비
    equip_comp = Equippable(EquipmentSlots.OUTFIT, sanity_resistance=10)
    coat = Entity(0,0,'[',tcod.purple,"trench coat", _Equippable=equip_comp)

    equip_comp = Equippable(EquipmentSlots.SCARF, sanity_resistance=20)
    scarf = Entity(0,0,'^',tcod.violet,"violet scarf", _Equippable=equip_comp)

    # 플레이어 컴포넌트
    f_comp = Fighter(hp=30, sanity=60, defense=10, power=15)
    i_comp = Inventory(26)
    e_comp = Equipment()

    hearn = Entity(0,0,'@',tcod.yellow,"Maribel Hearn", _Fighter=f_comp, _Inventory=i_comp, _Equipment=e_comp)

    # 장비 시도
    hearn._Inventory.add_item(scarf)
    results = hearn._Equipment.toggle_equip(scarf)
    hearn._Inventory.add_item(coat)
    hearn._Equipment.toggle_equip(coat)
    print(hearn._Equipment.total_sanity_resist)

