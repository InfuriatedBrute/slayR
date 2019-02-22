from enum import Enum


class Use_Case(Enum):
    active = 1
    onAttack = 2
    onDefend = 3


class Item:

    def __init__(self, use_function=None, use_case=Use_Case.active, consumable=False, prefix=None, targeted=False,
                 targeting_message={'message':'Choose a target'}, **kwargs):
        self.use_function = use_function
        self.targeting = targeted
        self.targeting_message = targeting_message
        self.use_case = use_case
        self.prefix = prefix
        self.consumable = consumable
        self.function_kwargs = kwargs
        
