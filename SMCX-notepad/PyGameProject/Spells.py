import pygame
from enum import Enum

class DamageType(Enum):
    ALMIGHTY = 0
    PHYSICAL = 1
    FIRE = 2
    ICE = 3
    ELECTRIC = 4
    WIND = 5
    PSYCHIC = 6
    NUCLEAR = 7
    BLESS = 8
    CURSE = 9
    
class DamageSpell():
    def __init__(self, name: str, damage_type: DamageType, cost: int = None, base_damage: int = None, spell_level: int = None, multi_target: bool = False):
        self.name = name
        self.damage_type = damage_type
        self.multi_target = multi_target
        if spell_level is not None:
            self.set_spell_level(spell_level)
        else:
            if cost is None or base_damage is None:
                raise ValueError("Only defined spell name and type")
            self.cost = cost
            self.base_damage = base_damage
            if self.multi_target:
                self.cost *= 2

    def set_spell_level(self, spell_level: int):
        if spell_level == 1:
            self.cost = 4
            self.base_damage = 15
        elif spell_level == 2:
            self.cost = 8
            self.base_damage = 40
        elif spell_level == 3:
            self.cost = 12
            self.base_damage = 60
        else:
            raise ValueError("Invalid spell level.")
        if self.multi_target:
            self.cost *= 2
    
    def use(self, magic_strength, target):
        damage = self.base_damage + round(self.base_damage * float(magic_strength) / 100) 
        
        if (self.multi_target):
            from Game import enemy_list
            for enemy in enemy_list:
                enemy.take_damage(damage)
        else:
            target.take_damage(damage)

class HealingSpell():
    def __init__(self, name: str, spell_level: int = None, multi_target: bool = False):
        self.name = name
        self.multi_target = multi_target
        self.set_spell_level(spell_level)
        
    def set_spell_level(self, spell_level: int):
        if spell_level == 1:
            self.cost = 4
            self.base_healing = 15
        elif spell_level == 2:
            self.cost = 8
            self.base_healing = 40
        elif spell_level == 3:
            self.cost = 12
            self.base_healing = 60
        else:
            raise ValueError("Invalid spell level.")
        if self.multi_target:
            self.cost *= 2
        
    def use(self, magic_strength, target):
        healing = self.base_healing + round(self.base_healing * float(magic_strength) / 100) 
        
        if (self.multi_target):
            from Game import party_list
            for member in party_list:
                member.heal(healing)
        else:
            target.heal(healing)

        
spell_dict = {
    "fire_1": DamageSpell("Agi", DamageType.FIRE, spell_level = 1),
    "ice_1": DamageSpell("Bufu", DamageType.ICE, spell_level = 1),
    "electro_1": DamageSpell("Zio", DamageType.ELECTRIC, spell_level = 1),
    "wind_1": DamageSpell("Garu", DamageType.WIND, cost=3, base_damage=12),
    "psychic_1": DamageSpell("Psy", DamageType.PSYCHIC, spell_level = 1),
    "nuke_1": DamageSpell("Frei", DamageType.NUCLEAR, spell_level = 1),
    "bless_1": DamageSpell("Kouha", DamageType.BLESS, spell_level = 1),
    "curse_1": DamageSpell("Eiha", DamageType.CURSE, spell_level = 1),
    "heal_1": HealingSpell("Dia", 1),
    "multi_fire_1": DamageSpell("Maragi", DamageType.FIRE, spell_level = 1, multi_target=True),
    "multi_ice_1": DamageSpell("Mabufu", DamageType.ICE, spell_level = 1, multi_target=True),
    "multi_electro_1": DamageSpell("Mazio", DamageType.ELECTRIC, spell_level = 1, multi_target=True),
    "multi_wind_1": DamageSpell("Magaru", DamageType.WIND, cost=3, base_damage=12, multi_target=True),
    "multi_psychic_1": DamageSpell("Mapsy", DamageType.PSYCHIC, spell_level = 1, multi_target=True),
    "multi_nuke_1": DamageSpell("Mafrei", DamageType.NUCLEAR, spell_level = 1, multi_target=True),
    "multi_bless_1": DamageSpell("Makouha", DamageType.BLESS, spell_level = 1, multi_target=True),
    "multi_curse_1": DamageSpell("Maeiha", DamageType.CURSE, spell_level = 1, multi_target=True),
    "multi_heal_1": HealingSpell("Media", 1, multi_target=True),
    }