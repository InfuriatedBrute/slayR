from game_messages import Message
from utils.initialize_all import initialize_all_pre
from components.item import Use_Case


class Fighter:

    @initialize_all_pre
    def __init__(self, base_hp, base_defense, base_power, xp=0, xpBounty=0):
        self.hp = base_hp
        
    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.attack_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xpBounty' : self.xpBounty})
        
        return results
        
    def heal(self, amount):
        results = []
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp
            
        return results
    
    
    def on_hit_effects(self, target,  game_map, entities):
        if self.owner.inventory:
            for item in self.owner.inventory.items:
                if(item.item.use_case == Use_Case.onAttack):
                    results, _ = self.owner.inventory.use(item, game_map, entities, target_x=target.x, target_y=target.y, triggered = True)
                    return results
        if target.inventory:
            for item in target.inventory.items:
                if(item.item.use_case == Use_Case.onDefend):
                    results, _ = target.inventory.use(item, game_map, entities, target_x=self.owner.x, target_y=self.owner.y, triggered = True)
                    return results
        return []
                    
                    

    def attack(self, target, game_map, entities):
        """Note that target is an entity"""
        results = []

        damage = self.power - target.fighter.defense
        
        results.extend(self.on_hit_effects(target, game_map, entities))

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)))})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name))})

        return results
    
