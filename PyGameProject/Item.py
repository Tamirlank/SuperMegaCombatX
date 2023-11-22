from audioop import mul
from enum import Enum
import pygame
from Character import Character

from Spells import DamageType

class ItemType(Enum):
    DAMAGE = 0,
    HEAL = 1,
    REVIVE = 2,
    MANA = 3,
    BUFF = 4,
    DEBUFF = 5

class Item():
    def __init__(self, name:str, item_type:ItemType, amount: int = 0, damage_type: DamageType = 0, multi_target: bool = False, count: int = 0):
        self.name = name
        self.item_type = type
        self.amount = amount
        self.damage_type = damage_type
        self.multi_target = multi_target
        self.count = count
        
    def use(self, target: Character):
        item_type = self.item_type
        if item_type == ItemType.HEAL or item_type == ItemType.REVIVE:
            target.heal(self.amount)
        elif item_type == ItemType.DAMAGE:
            target.take_damage(self.amount, self.damage_type, flat_damage=True)
        elif item_type == ItemType.MANA:
            target.restore_mana(self.amount)
