from entity import get_blocking_entity_at_location
from game_messages import Message


def activate_item_ability(item, owner, 
                           game_map, entities, target_x = None, target_y = None):
    results = []
    ap = item.ability_power

    if item.use_function == 'heal':
        target = get_blocking_entity_at_location(entities, target_x, target_y)
        results.append({'message' : Message("You heal " + target.name + " for " + str(ap) + " strength")})
        results.extend(target.fighter.heal(ap))

        
    if item.use_function == 'damage':
        target = get_blocking_entity_at_location(entities, target_x, target_y)
        results.append({'message' : Message("You damage " + target.name + " for " + str(ap) +"strength")})
        results.extend(target.fighter.take_damage(ap))

    return results