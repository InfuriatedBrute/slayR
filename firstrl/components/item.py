from enum import Enum
from utils.initialize_all import initialize_all_pre
from game_messages import Message


class Use_Case(Enum):
    active = 1
    onAttack = 2
    onDefend = 3


class Item:

    @initialize_all_pre
    def __init__(self, use_function=None, use_case=None, ability_power = None, consumable=False, prefix=None, targeted=False,
                 targeting_message=Message('Choose a target'), **kwargs):
        pass
        
