from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from loader_functions.constants import config, colors
from map_utils import GameMap, make_map
from render_functions import RenderOrder


def get_game_variables(settings=config):
    """Initializes the player entity, the game map, the message log, and the game state"""
    fighter_component = Fighter(base_hp=100, base_defense=1, base_power=2)
    inventory_component = Inventory(26)
    level_component = Level(level_up_base=settings['level_up_base'], level_up_factor=settings['level_up_factor'])
    equipment_component = Equipment()

    player = Entity(0, 0, '@', (255, 255, 255), 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, level=level_component,
                    equipment=equipment_component)
    entities = [player]

    game_map = GameMap(settings['map_width'], settings['map_height'])
    make_map(game_map, settings['max_rooms'], settings['room_min_size'],
             settings['room_max_size'], settings['map_width'], settings['map_height'], player, entities,
             colors)

    message_log = MessageLog(settings['message_x'], settings['message_width'],
                             settings['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
