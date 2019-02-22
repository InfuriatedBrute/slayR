from enum import Enum
from utils.initialize_all import initialize_all_pre


class Use_Case(Enum):
    active = 1
    onAttack = 2
    onDefend = 3


class Item:

    @initialize_all_pre
    def __init__(self, use_function=None, use_case=Use_Case.active, consumable=False, prefix=None, targeted=False,
                 targeting_message={'message':'Choose a target'}, **kwargs):
        pass
        
