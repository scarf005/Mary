from enum import Enum


class EquipmentSlots(Enum):
    WIELD = 1
    OUTFIT = 2
    SCARF = 3
    JEWELLERY = 4

    @classmethod
    def list_enums(cls, show="value"):
        if show == 'value':
            return list(map(lambda c: c.value, cls))
        elif show == 'name':
            return list(map(lambda c: c.name, cls))
