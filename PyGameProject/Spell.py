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
    
class Spell():
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
        

        
spell_list = {
    "Fire1": Spell("Agi", DamageType.FIRE, spell_level = 1),
    "Ice1": Spell("Bufu", DamageType.ICE, spell_level = 1),
    "Electro1": Spell("Zio", DamageType.ELECTRIC, spell_level = 1),
    "Wind1": Spell("Garu", DamageType.WIND, cost=3, base_damage=12),
    "Psychic1": Spell("Psy", DamageType.PSYCHIC, spell_level = 1),
    "Nuke1": Spell("Frei", DamageType.NUCLEAR, spell_level = 1),
    "Bless1": Spell("Kouha", DamageType.BLESS, spell_level = 1),
    "Curse1": Spell("Eiha", DamageType.CURSE, spell_level = 1),
    }