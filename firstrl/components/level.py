from loader_functions.constants import config
from utils.initialize_all import initialize_all_pre


class Level:

    @initialize_all_pre
    def __init__(self, level_up_base=config['level_up_base'], level_up_factor=config['level_up_factor'], current_level=1, current_xp=0):
        pass

    @property
    def experience_to_next_level(self):
        return self.level_up_base + self.current_level * self.level_up_factor

    def add_xp(self, xp):
        self.current_xp += xp

        if self.current_xp > self.experience_to_next_level:
            self.current_xp -= self.experience_to_next_level
            self.current_level += 1

            return True
        else:
            return False
        
