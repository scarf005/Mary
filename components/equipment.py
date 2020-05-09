from enums.equipment_slots import EquipmentSlots

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
                #print(equip)
                equippable = getattr(equip, '_Equippable', None)
                bonus = getattr(equippable, equippable_value, None)
                if bonus: V += bonus

        return V

    @property
    def total_sanity_resist(self):
        return self.get_total_bonus('sanity_resistance')

    def toggle_equip(self, equippable_entity):
        results = []

        enum_slots_list = EquipmentSlots.list_enums()
        slot = equippable_entity._Equippable.slot
        for enum in EquipmentSlots:
            if slot == enum:
                search = str(enum.name.lower())
                self_slot_value = getattr(self, search, None)

                if self_slot_value == equippable_entity: # 손에 든 물건 빼기
                    setattr(self, search, None)
                    equippable_entity._Equippable.equipped = False
                    results.append({'dequipped': equippable_entity})
                else:
                    if self_slot_value: # 기존에 들던 물건 빼기
                        equippable_entity._Equippable.equipped = False
                        results.append({'dequipped': self_slot_value})

                    setattr(self, search, equippable_entity) # 바꿔치기
                    equippable_entity._Equippable.equipped = True
                    results.append({'equipped': equippable_entity})
                break

        return results