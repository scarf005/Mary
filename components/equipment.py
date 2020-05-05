from equipment_slots import EquipmentSlots

class Equipments:
    def __init__(self, slot, **kwargs):
        """
        장비 판 인벤토리.
        """
        # 기타 속성들
        slots_list = {'wielding':None, 'outfit':None, 'scarf':None, 'jewellery':None}
        total_list = {**slots_list}
        for key,value in total_list.items():
            if key in kwargs.keys():
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, value)

    @property
    def total_sanity_resist(self):
        R = 0
        if self.owner:
            for equipment in self.slots_list:
                print(equipment)
                """
                equip = getattr(self, equipment, None)
                print(equip)
                if equip:
                    print(equip)
                """
        return R