from game_messages import Message
import item_functions


class Inventory:

    def __init__(self, capacity):
        self.capacity = capacity
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

    def use(self, item_entity, colors, game_map, entities, target_x=None, target_y=None):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None or item_entity.equippable:
            equippable_component = item_entity.equippable

            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message('The {0} cannot be used'.format(item_entity.name),
                                                   colors.get('yellow'))})
        else:
            if item_component.targeting and not (target_x or target_y):
                # Item still needs to be targeted
                results.append({'targeting': item_entity})
            else:
                if not target_x and not target_y:  # and not item_component.targeting
                    target_x = self.owner.x
                    target_y = self.owner.y
                item_use_results = item_functions.activate_item_ability(item=item_component, owner=self.owner, entities=entities,
                                                                         target_x=target_x, target_y=target_y, game_map=game_map)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)

                results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)
        
    def drop_item(self, item, colors):
        results = []
        
        if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
            self.owner.equipment.toggle_equip(item)

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message('You dropped the {0}'.format(item.name),
                                                                 colors.get('yellow'))})

        return results
