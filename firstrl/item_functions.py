from entity import get_blocking_entity_at
from game_messages import Message


def activate_item_ability(item, owner, 
                           game_map, entities, target_x = None, target_y = None):
    results = []
    ap = item.ability_power
    target = get_blocking_entity_at(entities, target_x, target_y)

    if item.use_function == 'heal' and target:
        results.append({'message' : Message("You heal " + target.name + " for " + str(ap) + " strength")})
        results.extend(target.fighter.heal(ap))

        
    if item.use_function == 'damage' and target:
        results.append({'message' : Message("You damage " + target.name + " for " + str(ap) +" strength")})
        results.extend(target.fighter.take_damage(ap))

    return results