import math

from components.item import Item
from render_functions import RenderOrder
from utils.initialize_all import initialize_all_post


class Entity:
    """A generic object to represent players, enemies, items, etc."""

    @initialize_all_post
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 item=None, inventory=None, stairs=None, level=None, equipment=None, equippable=None, unique=False):
        
        if equippable and not item:
            item = Item()
            
        components = {fighter, ai, item, inventory, stairs, level, equipment, equippable}
        
        for c in components:
            if c:
                c.owner = self



    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        path = game_map.compute_path(self.x, self.y, target_x, target_y)

        dx = path[0][0] - self.x
        dy = path[0][1] - self.y

        if game_map.walkable[path[0][0], path[0][1]] and not get_blocking_entity_at_location(entities, self.x + dx,
                                                                                               self.y + dy):
            self.move(dx, dy)
            
    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to(self, other):
        return self.distance(other.x, other.y)


def get_blocking_entity_at_location(entities, destination_x, destination_y):
    if entities is None:
        return None
    toReturn = [entity for entity in entities if entity.x == destination_x and 
            entity.y == destination_y and  entity.blocks]
    return toReturn[0] if toReturn else None
