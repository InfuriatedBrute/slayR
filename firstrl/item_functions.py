from entity import get_blocking_entity_at_location


def activate_item_ability(item, owner, 
                           game_map, entities, target_x = None, target_y = None):
    results = []

    if item.use_function == 'heal':
        target = get_blocking_entity_at_location(entities, target_x, target_y)
        results.extend(target.fighter.heal(5))
        #results.append({'consumed': True, 'message': Message('It hurts!', colors.get('black'))})
        
    if item.use_function == 'damage':
        target = get_blocking_entity_at_location(entities, target_x, target_y)
        results.extend(target.fighter.take_damage(5))

    return results