from components.equipment_slots import EquipmentSlots



class Equipment:
    
    def __init__(self, *equippable_entities):
        for slotType in EquipmentSlots:
            slotSet = False
            for equippable_entity in equippable_entities:
                if not slotSet and equippable_entity.equippable.slot.equals(slotType):
                    setattr(self, slotType.name, equippable_entity)
                    slotSet = True
            if not slotSet:
                setattr(self, slotType.name, None)
        
        
    def _sum_of_stat(self, stat):
        bonus = 0
        for slot_type in EquipmentSlots:
            item_in_slot = getattr(self, slot_type.name)
            if item_in_slot is not None and item_in_slot.equippable:
                toAdd = getattr(item_in_slot.equippable, stat)
                if toAdd:
                    bonus+= toAdd
        return bonus

    @property
    def max_hp_bonus(self):
        return self._sum_of_stat('max_hp_bonus')

    @property
    def attack_bonus(self):
        return self._sum_of_stat('attack_bonus')

    @property
    def defense_bonus(self):
        return self._sum_of_stat('defense_bonus')

    def toggle_equip(self, equippable_entity):
        results = []
        slot = equippable_entity.equippable.slot.name
        #If the item is equipped dequip it
        if getattr(self, slot) == equippable_entity:
            setattr(self, slot, None)
            results.append({'dequipped': equippable_entity})
        #Else equip the new and dequip the old
        else:
            if getattr(self, slot):
                results.append({'dequipped': getattr(self, slot)})
            setattr(self, slot, equippable_entity)
            results.append({'equipped': equippable_entity})
        return results