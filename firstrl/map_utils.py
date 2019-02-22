import json
from random import randint, shuffle

from tdl.map import Map

from components.ai import BasicMonster
from components.equipment_slots import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.item import Use_Case
from components.stairs import Stairs
from entity import Entity
from game_messages import Message
from loader_functions.constants import config, colors, items, item_prefixes, enchantments
from random_utils import random_choice_from_dict, from_dungeon_level
from render_functions import RenderOrder


class GameMap(Map):
    """Map with altered constructor and the dungeon_level variable."""

    def __init__(self, width, height, dungeon_level=1):
        super().__init__(width, height)
        self.explored = [[config['wallhack'] for _y in range(height)] for _x in range(width)]

        self.dungeon_level = dungeon_level


class Rect:

    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


def create_room(game_map, room):
    # go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            game_map.walkable[x, y] = True
            game_map.transparent[x, y] = True


def create_h_tunnel(game_map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True


def create_v_tunnel(game_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True


def place_entities(room, entities, dungeon_level, colors, num_monsters):
    max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], dungeon_level)  # Get a random number of monsters
    num_items = randint(0, max_items_per_room)
    
    for _i in range(num_monsters):
        # Choose a random location in the room
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            fighter_component = Fighter(hp=10, defense=0, power=3, xpBounty=35)
            ai_component = BasicMonster()

            monster = Entity(x, y, 'o', colors.get('desaturated_green'), 'Orc', blocks=True,
                render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component, god=True)

            entities.append(monster)

    for _i in range(num_items):
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)
        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            itemData = random_choice_from_dict(items, 'drop_weight')
            enchantment = random_choice_from_dict(enchantments, 'drop_weight')
            prefix = random_choice_from_dict(item_prefixes, 'drop_weight')
            
            color = colors.get(enchantment['color'])
            icon = itemData['icon']
            tags = itemData['tags']
            if 'totem' in tags:
                raise NotImplementedError
            while('consumable' in tags and enchantment['consumable_name'] is None):
                # No mundane consumables allowed
                enchantment = random_choice_from_dict(enchantments, 'drop_weight')
    
            print("\nData: " + json.dumps(itemData) + "\nEnchantment: " + json.dumps(enchantment) + "\nPrefix: " + json.dumps(prefix))
            
            attack_bonus = itemData.get('attack_bonus')
            defense_bonus = itemData.get('defense_bonus')
            max_hp_bonus = itemData.get('max_hp_bonus')
            targeted = 'targeted' in tags
            if 'active' in tags:
                use_case = Use_Case.active
                equippable_component = None
            elif 'weapon' in tags:
                equippable_component = Equippable(EquipmentSlots.MAIN_HAND, attack_bonus, defense_bonus, max_hp_bonus)
                use_case = Use_Case.onAttack
            elif 'armor' in tags:
                equippable_component = Equippable(EquipmentSlots.BODY, attack_bonus, defense_bonus, max_hp_bonus)
                use_case = Use_Case.onDefend
            else:
                equippable_component = None
                use_case = None
            if(enchantment['function_name'] == ""):
                use_case = None
            item_name = enchantment['consumable_name'] if 'consumable' in tags else prefix['name'] + '' + itemData['name'] + '' + enchantment['adjective']
            item = Entity(x, y, icon, color, item_name, equippable=equippable_component, render_order=RenderOrder.ITEM,
                item=Item(use_case=use_case, use_function=enchantment['function_name'], consumable=('consumable' in tags), targeted=targeted, prefix=prefix))

            entities.append(item)
 

def make_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, colors):
    rooms = []
    num_rooms = 0

    center_of_last_room_x = None
    center_of_last_room_y = None

    for _r in range(max_rooms):
        # random width and height
        w = randint(room_min_size, room_max_size)
        h = randint(room_min_size, room_max_size)
        # random position without going out of the boundaries of the map
        x = randint(0, map_width - w - 1)
        y = randint(0, map_height - h - 1)

        # "Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)

        # run through the other rooms and see if they intersect with this one
        for other_room in rooms:
            if new_room.intersect(other_room):
                break
        else:
            # this means there are no intersections, so this room is valid

            # "paint" it to the map's tiles
            create_room(game_map, new_room)

            # center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()

            center_of_last_room_x = new_x
            center_of_last_room_y = new_y

            if num_rooms == 0:
                # this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y
            else:
                # all rooms after the first:
                # connect it to the previous room with a tunnel

                # center coordinates of previous room
                (prev_x, prev_y) = rooms[num_rooms - 1].center()

                # flip a coin (random number that is either 0 or 1)
                if randint(0, 1) == 1:
                    # first move horizontally, then vertically
                    create_h_tunnel(game_map, prev_x, new_x, prev_y)
                    create_v_tunnel(game_map, prev_y, new_y, new_x)
                else:
                    # first move vertically, then horizontally
                    create_v_tunnel(game_map, prev_y, new_y, prev_x)
                    create_h_tunnel(game_map, prev_x, new_x, new_y)
                    
            # finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1
            
    shuffle(rooms)
    placed_monsters = 0
    for room in rooms:
        if(placed_monsters < config['max_monsters_per_floor']):
            num_monsters = 1
        else:
            num_monsters = 0
        place_entities(room, entities, game_map.dungeon_level, colors, num_monsters)
        placed_monsters += 1

    stairs_component = Stairs(game_map.dungeon_level + 1)
    down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', (255, 255, 255), 'Stairs',
                         render_order=RenderOrder.STAIRS, stairs=stairs_component)
    print(down_stairs)
    entities.append(down_stairs)

    
def next_floor(player, message_log, dungeon_level, config):
    """The functions creates a brand new GameMap, with the dungeon level being increased by one.
     The entities list is created from scratch as well, with only the player in it initially. 
     We then call make_map to generate the new floor, like we did at the game's start. 
     We'll also give the player half of the max HP back, as a reward for making it to the new floor, 
     and add a message to this effect. We then return the game_map and entities to be used in engine.py."""
     
    game_map = GameMap(config['map_width'], config['map_height'], dungeon_level)
    entities = [player]

    make_map(game_map, config['max_rooms'], config['room_min_size'],
             config['room_max_size'], config['map_width'], config['map_height'], player, entities,
             colors)

    player.fighter.heal(player.fighter.max_hp // 2)

    message_log.add_message(Message('You take a moment to rest, and recover your strength.',
                                    colors.get('light_violet')))

    return game_map, entities
