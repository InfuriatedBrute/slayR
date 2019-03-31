from game_messages import Message
import item_functions
from utils.initialize_all import initialize_all_pre
from loader_functions.constants import colors
from components.equipment_slots import EquipmentSlots

class Inventory:

    @initialize_all_pre
    def __init__(self, capacity):
        self.items = []

    def add_item(self, item, colors):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full', colors.get('yellow'))
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}!'.format(item.name), colors.get('blue'))
            })

            self.items.append(item)

        return results

    def use(self, item_entity, game_map, entities, target_x=None, target_y=None, triggered = False):
        results = []
        next_turn = False

        item_component = item_entity.item

        if item_component.use_function is None or (item_entity.equippable and not triggered):
            equippable_component = item_entity.equippable

            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message('The {0} cannot be used'.format(item_entity.name),
                                                   colors.get('yellow'))})
        else:
            if item_component.targeted and not (target_x or target_y): # Item still needs to be targeted
                results.append({'targeting': item_entity})
            else:
                if not target_x and not target_y:  # and not item_component.targeted
                    target_x = self.owner.x
                    target_y = self.owner.y
                item_use_results = item_functions.activate_item_ability(item=item_component, owner=self.owner, entities=entities,
                                                                         target_x=target_x, target_y=target_y, game_map=game_map)

                item_use_results_except_consumed = list(filter(lambda x : not x.get('consumed'), item_use_results))
                results.extend(item_use_results_except_consumed)
                next_turn = True

        return results, next_turn

    def remove_item(self, item):
        self.items.remove(item)
        
    def drop_item(self, item, colors):
        results = []
        for slot in EquipmentSlots:
            if getattr(self.owner.equipment, slot.name) == item:
                self.owner.equipment.toggle_equip(item)
                break

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message('You dropped the {0}'.format(item.name),
                                                                 colors.get('yellow'))})

        return results
