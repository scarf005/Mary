from equipment_slots import EquipmentSlots

class Equipment:
    def __init__(self, **kwargs):
        """
        장비 판 인벤토리.
        """
        # 이 캐릭터가 장비할 수 있는 물건들의 종류
        self.slots_list = {'wield':None, 'outfit':None, 'scarf':None, 'jewellery':None}
        total_list = {**self.slots_list}
        for key,value in total_list.items():
            if key in kwargs.keys():
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, value)

    def get_total_bonus(self, equippable_value):
        V = 0
        if self.owner:
            for equipment in self.slots_list:
                # 가지고 있는 장비가 있는지 확인
                equip = getattr(self, equipment, None)
                equippable = getattr(equip, '_Equippable', None)
                temp = getattr(equippable, equippable_value, None)
                if temp: V += temp

        return V

    @property
    def total_sanity_resist(self):
        return self.get_total_bonus('sanity_resistance')

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity._Equippable.slot

        if slot == EquipmentSlots.SCARF:
            if self.scarf == equippable_entity:
                self.scarf = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.scarf: # 바꿔치기
                    results.append({'dequipped': self.scarf})

                self.scarf = equippable_entity
                results.append({'equipped': equippable_entity})

        return results