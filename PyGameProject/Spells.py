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
    pass

class DamageSpell(Spell):
    def __init__(self, name: str, damage_type: DamageType, sprite: str = None, sprite_scale: float = 1, 
                 cost: int = None, base_damage: int = None, 
                 spell_level: int = None, 
                 multi_target: bool = False):
        self.name = name
        self.damage_type = damage_type
        self.multi_target = multi_target
        self.sprite = sprite
        self.sprite_scale = sprite_scale

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
            self.base_damage = 10
        elif spell_level == 2:
            self.cost = 8
            self.base_damage = 25
        elif spell_level == 3:
            self.cost = 12
            self.base_damage = 60
        else:
            raise ValueError("Invalid spell level.")
        if self.multi_target:
            self.cost *= 2
    
    def use(self, damage_bonus, target, caster):
        import MovingImage
        from Game import moving_images
        
        damage = self.base_damage + round(self.base_damage * float(damage_bonus) / 100) 


        if (self.multi_target):
            from Game import battle
            if caster.is_enemy:
                for member in battle.party_list:
                    member.take_damage(damage, self.damage_type)
                    MovingImage.animate(self.sprite, caster.x, caster.y, member.x, member.y, self.sprite_scale)
            else:
                for member in battle.enemy_list:
                    if member.alive:
                        member.take_damage(damage, self.damage_type)
                        MovingImage.animate(self.sprite, caster.x, caster.y, member.x, member.y, self.sprite_scale)
        else:
            target.take_damage(damage, self.damage_type)
            MovingImage.animate(self.sprite, caster.x, caster.y, target.x, target.y, self.sprite_scale)

class HealingSpell(Spell):
    def __init__(self, name: str, sprite: str = None, sprite_scale: float = 1,
                 spell_level: int = None, 
                 cost:int=0,
                 multi_target: bool = False, 
                 revives: bool = False):
        self.name = name
        self.multi_target = multi_target
        self.spell_level = spell_level
        if cost == 0:
            self.set_spell_level(spell_level)
        else:
            self.cost = cost
        self.revives = revives     
        self.sprite = sprite
        self.sprite_scale = sprite_scale

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
        
    def use(self, magic_strength, target, caster):
        import MovingImage
        
        if self.revives:
            if self.spell_level == 1:
                percentage = 0.1
            elif self.spell_level == 2:
                percentage = 0.5
            else:
                percentage = 1
            MovingImage.animate(self.sprite, target.x, target.y, target.x, target.y, self.sprite_scale)
            target.heal(round(target.max_hp * percentage))
            return
        
        healing = self.base_healing + round(self.base_healing * float(magic_strength) / 100) 
        
        if (self.multi_target):
            from Game import battle
            if caster.is_enemy:
                for member in battle.enemy_list:
                    member.heal(healing)
                    MovingImage.animate(self.sprite, caster.x, caster.y, member.x, member.y, self.sprite_scale)
            else:
                for member in battle.party_list:
                    if member.alive:
                        member.heal(healing)
                        MovingImage.animate(self.sprite, caster.x, caster.y, member.x, member.y, self.sprite_scale)
        else:
            target.heal(healing)
            MovingImage.animate(self.sprite, caster.x, caster.y, target.x, target.y, self.sprite_scale)
        
spell_dict = {
    "phys_1": DamageSpell("Cleave", DamageType.PHYSICAL, cost=8, base_damage=20),
    "fire_1": DamageSpell("Agi", DamageType.FIRE, 'Attacks/Fireball.png', 5, spell_level = 1),
    "ice_1": DamageSpell("Bufu", DamageType.ICE, 'Attacks/Icicle.png', 3, spell_level = 1),
    "electro_1": DamageSpell("Zio", DamageType.ELECTRIC, 'Attacks/Electro.png', 3, spell_level = 1),
    "wind_1": DamageSpell("Garu", DamageType.WIND, 'Attacks/Wind.png', 3,  cost=3, base_damage=12),
    "psychic_1": DamageSpell("Psi", DamageType.PSYCHIC, 'Attacks/Psychic.png', 3,  spell_level = 1),
    "nuke_1": DamageSpell("Frei", DamageType.NUCLEAR, 'Attacks/Nuke.png', 3,  spell_level = 1),
    "bless_1": DamageSpell("Kouha", DamageType.BLESS, 'Attacks/Bless.png', 3,  spell_level = 1),
    "curse_1": DamageSpell("Eiha", DamageType.CURSE, 'Attacks/Curse.png', 2.5, spell_level = 1),
    "heal_1": HealingSpell("Dia", 'Attacks/Heart.png', 3, spell_level = 1),
    "revive_1": HealingSpell("Revivify", 'Attacks/Revive.png', 4.5, spell_level = 2, revives=True),
    "multi_fire_1": DamageSpell("Maragi", DamageType.FIRE, 'Attacks/Fireball.png', 5, spell_level = 1, multi_target=True),
    "multi_ice_1": DamageSpell("Mabufu", DamageType.ICE, 'Attacks/Icicle.png', 3, spell_level = 1, multi_target=True),
    "multi_electro_1": DamageSpell("Mazio", DamageType.ELECTRIC, 'Attacks/Electro.png', 3, spell_level = 1, multi_target=True),
    "multi_wind_1": DamageSpell("Magaru", DamageType.WIND, 'Attacks/Wind.png', 3,  cost=3, base_damage=12, multi_target=True),
    "multi_psychic_1": DamageSpell("Mapsy", DamageType.PSYCHIC, 'Attacks/Psychic.png', 3,  spell_level = 1, multi_target=True),
    "multi_nuke_1": DamageSpell("Mafrei", DamageType.NUCLEAR, 'Attacks/Nuke.png', 2,  spell_level = 1, multi_target=True),
    "multi_bless_1": DamageSpell("Makouha", DamageType.BLESS, 'Attacks/Bless.png', 3,  spell_level = 1, multi_target=True),
    "multi_curse_1": DamageSpell("Maeiha", DamageType.CURSE, 'Attacks/Curse.png', 2.5, spell_level = 1, multi_target=True),
    "multi_heal_1": HealingSpell("Media", 'Attacks/Heart.png', 3, spell_level = 1, multi_target=True),
    }

spell_dict_2 = {
    "phys_2": DamageSpell("Crush", DamageType.PHYSICAL, cost=24, base_damage=40),
    "fire_2": DamageSpell("Agilao", DamageType.FIRE, 'Attacks/Fireball.png', 5, spell_level = 2),
    "ice_2": DamageSpell("Bufula", DamageType.ICE, 'Attacks/Icicle.png', 4, spell_level = 2),
    "electro_2": DamageSpell("Zionga", DamageType.ELECTRIC, 'Attacks/Electro.png', 4, spell_level = 2),
    "wind_2": DamageSpell("Garuda", DamageType.WIND, 'Attacks/Wind.png', 4,  cost=6, base_damage=22),
    "psychic_2": DamageSpell("Psio", DamageType.PSYCHIC, 'Attacks/Psychic.png', 4,  spell_level = 2),
    "nuke_2": DamageSpell("Freila", DamageType.NUCLEAR, 'Attacks/Nuke.png', 4,  spell_level = 2),
    "bless_2": DamageSpell("Kouga", DamageType.BLESS, 'Attacks/Bless.png', 4,  spell_level = 2),
    "curse_2": DamageSpell("Eiga", DamageType.CURSE, 'Attacks/Curse.png', 2.5, spell_level = 2),
    "heal_2": HealingSpell("Diarama", 'Attacks/Heart.png', 4, spell_level = 2),
    "revive_2": HealingSpell("Revivify", 'Attacks/Revive.png', 4.5, cost=12, revives=True),
    "multi_fire_2": DamageSpell("Maragilao", DamageType.FIRE, 'Attacks/Fireball.png', 5, spell_level = 2, multi_target=True),
    "multi_ice_2": DamageSpell("Mabufula", DamageType.ICE, 'Attacks/Icicle.png', 4, spell_level = 2, multi_target=True),
    "multi_electro_2": DamageSpell("Mazionga", DamageType.ELECTRIC, 'Attacks/Electro.png', 4, spell_level = 2, multi_target=True),
    "multi_wind_2": DamageSpell("Magaruda", DamageType.WIND, 'Attacks/Wind.png', 4,  cost=6, base_damage=22, multi_target=True),
    "multi_psychic_2": DamageSpell("Mapsio", DamageType.PSYCHIC, 'Attacks/Psychic.png', 4,  spell_level = 2, multi_target=True),
    "multi_nuke_2": DamageSpell("Mafreila", DamageType.NUCLEAR, 'Attacks/Nuke.png', 3,  spell_level = 2, multi_target=True),
    "multi_bless_2": DamageSpell("Makouga", DamageType.BLESS, 'Attacks/Bless.png', 4,  spell_level = 2, multi_target=True),
    "multi_curse_2": DamageSpell("Maeiga", DamageType.CURSE, 'Attacks/Curse.png', 2.5, spell_level = 2, multi_target=True),
    "multi_heal_2": HealingSpell("Mediarama", 'Attacks/Heart.png', 3, spell_level = 2, multi_target=True),
    }
spell_dict_3 = {
    "phys_3": DamageSpell("God's Hand", DamageType.PHYSICAL, cost=38, base_damage=70),
    "fire_3": DamageSpell("Agidyne", DamageType.FIRE, 'Attacks/Fireball.png', 5, spell_level = 3),
    "ice_3": DamageSpell("Bufudyne", DamageType.ICE, 'Attacks/Icicle.png', 5, spell_level = 3),
    "electro_3": DamageSpell("Ziodyne", DamageType.ELECTRIC, 'Attacks/Electro.png', 5, spell_level = 3),
    "wind_3": DamageSpell("Garudyne", DamageType.WIND, 'Attacks/Wind.png', 5,  cost=12, base_damage=52),
    "psychic_3": DamageSpell("Psiodyne", DamageType.PSYCHIC, 'Attacks/Psychic.png', 5,  spell_level = 3),
    "nuke_3": DamageSpell("Freidyne", DamageType.NUCLEAR, 'Attacks/Nuke.png', 5,  spell_level = 3),
    "bless_3": DamageSpell("Kougaon", DamageType.BLESS, 'Attacks/Bless.png', 5,  spell_level = 3),
    "curse_3": DamageSpell("Eigaon", DamageType.CURSE, 'Attacks/Curse.png', 2.5, spell_level = 3),
    "heal_3": HealingSpell("Diarahan", 'Attacks/Heart.png', 5, spell_level = 3),
    "revive_3": HealingSpell("Revivify", 'Attacks/Revive.png', 5.5, cost=24, revives=True),
    "multi_fire_3": DamageSpell("Maragidyne", DamageType.FIRE, 'Attacks/Fireball.png', 5, spell_level = 3, multi_target=True),
    "multi_ice_3": DamageSpell("Mabufudyne", DamageType.ICE, 'Attacks/Icicle.png', 5, spell_level = 3, multi_target=True),
    "multi_electro_3": DamageSpell("Maziodyne", DamageType.ELECTRIC, 'Attacks/Electro.png', 5, spell_level = 3, multi_target=True),
    "multi_wind_3": DamageSpell("Magarudyne", DamageType.WIND, 'Attacks/Wind.png', 5,  cost=12, base_damage=32, multi_target=True),
    "multi_psychic_3": DamageSpell("Mapsiodyne", DamageType.PSYCHIC, 'Attacks/Psychic.png', 5,  spell_level = 3, multi_target=True),
    "multi_nuke_3": DamageSpell("Mafreidyne", DamageType.NUCLEAR, 'Attacks/Nuke.png', 5,  spell_level = 3, multi_target=True),
    "multi_bless_3": DamageSpell("Makougaon", DamageType.BLESS, 'Attacks/Bless.png', 5,  spell_level = 3, multi_target=True),
    "multi_curse_3": DamageSpell("Maeigaon", DamageType.CURSE, 'Attacks/Curse.png', 2.5, spell_level = 3, multi_target=True),
    "multi_heal_3": HealingSpell("Mediarahan", 'Attacks/Heart.png', 5, spell_level = 3, multi_target=True),
    }