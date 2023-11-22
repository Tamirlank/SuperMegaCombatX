from math import floor
import pygame
from Spells import DamageType, spell_dict, DamageSpell, spell_dict_2, spell_dict_3
import random


class Character:
    weaknesses: DamageType = []
    resists: DamageType = []
    nullifies: DamageType = []
    drains: DamageType = []
    spells: DamageSpell = []

    x: float
    y: float

    name: str
    max_hp: int

    base_damage: int

    mana: int
    max_mana: int

    strength: int
    magic_strength: int
    armor: int
    agility: int
    luck: int

    sprite: str
    scale: float
    
    downed: bool = False       
    is_enemy: bool = None
    is_ai: bool = True

    def __init__(self, **kwargs):
        self.x = 0
        self.y = 225
        self.raised_y = self.y - 25
        
        self.name = kwargs.get('name', '')
        self.sprite = kwargs.get('sprite', '')
        self.scale = kwargs.get('scale', 1.0)
        self.max_hp = kwargs.get('max_hp', 100)
        self.max_mana = kwargs.get('max_mana', 100)
        self.base_damage = kwargs.get('base_damage', 10)
        self.strength = kwargs.get('strength', 5)
        self.magic_strength = kwargs.get('magic_strength', 5)
        self.armor = kwargs.get('armor', 5)
        self.agility = kwargs.get('agility', 5)
        self.luck = kwargs.get('luck', 5)
        self.spells = kwargs.get('spells', [])
        self.weaknesses = kwargs.get('weaknesses', [])
        self.resists = kwargs.get('resists', [])
        self.nullifies = kwargs.get('nullifies', [])
        self.drains = kwargs.get('drains', [])
        self.is_ai = kwargs.get('is_ai', True)

        self.damage_timer = 0
        self.attack_timer = 20
        self.pass_timer = 0

        self.downed = False        

        self.initiative_index = 0
        self.party_index = 0
        
        self.hp = self.max_hp
        self.mana = self.max_mana

        self.alive = True

        self.defending = False

        self.image = pygame.image.load(self.sprite)
        self.image = pygame.transform.scale_by(self.image, self.scale)
        self.rect = self.image.get_rect()
        
        self.downed_image = pygame.image.load('Downed.png')
        self.downed_image = pygame.transform.scale_by(self.downed_image, 5)
        self.downed_rect = self.downed_image.get_rect()
        self.downed_rect.center = (self.x, self.y - 100)
        
        self.shield_image = pygame.image.load('Attacks/Shield.png')
        self.shield_image = pygame.transform.scale_by(self.shield_image, 5)
        self.shield_rect = self.shield_image.get_rect()
        self.shield_rect.center = (self.x, self.y+20)
        
        self.pass_image = pygame.image.load('Pass.png')
        self.pass_image = pygame.transform.scale_by(self.pass_image, 1.75)
        self.pass_rect = self.pass_image.get_rect()
        self.pass_rect.center = (self.x, self.y - 20)

    def refactor_position(self, enemy_list, party_list):
        from Game import screenWidth

        middle = screenWidth / 2
        if self.is_enemy:
            spacing = middle / (len(enemy_list) + 1)
            i = 1
            taken_positions = [float(pos.x) for pos in enemy_list]
            while float(middle + spacing * i) in taken_positions:
                i += 1
            self.x = middle + spacing * i

        else:
            spacing = middle / (len(party_list) + 1)
            i = 1
            taken_positions = [float(pos.x) for pos in party_list]
            while float(spacing * i) in taken_positions and self:
                i += 1
            self.x = spacing * i
            
        self.downed_rect.center = (self.x, self.y - 100)
        
        self.shield_rect.center = (self.x, self.y + 20)
        
        self.pass_rect.center = (self.x, self.y + 10)

    def draw(self, initiative, current_character):
        from Game import screen
        
        self.damage_timer -= 1
        self.attack_timer -= 1
        self.pass_timer -= 1

        if self.damage_timer == 0:
            self.image = pygame.image.load(self.sprite)
            self.image = pygame.transform.scale_by(self.image, self.scale)
            self.rect = self.image.get_rect()
            
        if current_character == self:
            self.rect.center = (self.x, self.raised_y)
        else:
            self.rect.center = (self.x, self.y)
            
        if self.pass_timer > 0:
            screen.blit(self.pass_image, self.pass_rect)
            
        if self.attack_timer < 0:
            screen.blit(self.image, self.rect)
        
        if self.downed:
            screen.blit(self.downed_image, self.downed_rect)

        if self.defending:
            screen.blit(self.shield_image, self.shield_rect)

    def take_damage(self, damage: int, damage_type: DamageType = 0, flat_damage: bool = False):
        from Game import battle
        import UI
        
        self.damage_timer = 20
        self.image.fill((190, 0, 0, 100), special_flags=pygame.BLEND_ADD)
        
        if flat_damage:
            amount = damage
            if damage_type in self.weaknesses:
                if not self.downed:
                    self.downed = True
                    if self.is_enemy:
                        battle.pass_available = True
                        UI.cutin_timer = 20
                    else:
                        if self in battle.available_passes:
                            battle.available_passes.remove(self)
            
        else:
            damage_amount = damage
            if damage_type in self.nullifies:
                damage_amount = 0
            elif damage_type in self.drains:
                self.heal(damage_amount)
                return
            elif damage_type in self.resists:
                damage_amount = damage_amount // 2
            
            if self.defending:
                damage_amount = damage_amount // 2
            elif damage_type in self.weaknesses:
                if not self.downed:
                    self.downed = True
                    if self.is_enemy:
                        battle.pass_available = True
                        UI.cutin_timer = 20
                    else:
                        if self in battle.available_passes:
                            battle.available_passes.remove(self)
                damage_amount = damage_amount * 2

            amount = round(float(damage_amount) * (1 - float(self.armor) / 200))

        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.die()

    def attack(self, target):
        from Game import battle
        import Utilities

        offset = 30
        if self.is_enemy:
            offset = offset * -1
        attack_animation_speed = 20        

        Utilities.animate(self.sprite, self.x + offset, self.y, self.x, self.y, self.scale, attack_animation_speed)
        self.attack_timer = attack_animation_speed
        battle.pass_available = False
        target.take_damage(self.base_damage + round(self.base_damage * float(self.strength) / 100), DamageType.PHYSICAL)
        battle.next_turn()

    def ai_logic(self):
        from Game import battle
        available_spells = []
        for spell in self.spells:
            if spell.cost < self.mana:
                available_spells.append(spell)
                
        if available_spells:
            if random.randint(1, 100) <= 75:
                self.random_spell(available_spells)
                return
        self.random_attack()

    def random_attack(self):
        from Game import battle

        if self.is_enemy:
            target = self.choose_random_player()
        else:
            target = random.choice(battle.enemy_list)

        self.attack(target)

    def random_spell(self, available_spells):
        from Game import battle
        selected_spell = random.choice(available_spells)
        print(selected_spell.name)
        if self.is_enemy:
            if isinstance(selected_spell, DamageSpell):
                target = self.choose_random_player()
            else:
                target = self.heal_weakest_ally()
                
        else:
            if isinstance(selected_spell, DamageSpell):
                target = random.choice(battle.enemy_list)
            else:
                target = self.choose_random_player()
        self.use_spell(selected_spell, target)
        
    def heal_weakest_ally(self):
        from Game import battle
        weakest_ally = self
        if self.is_enemy:
            for enemy in battle.enemy_list:
                if enemy.hp < weakest_ally.hp:
                    weakest_ally = enemy
        else:
            for ally in battle.party_list:
                if ally.hp < weakest_ally.hp:
                    weakest_ally = ally
        return weakest_ally

    def choose_random_player(self):
        from Game import battle

        available_targets = []
        for ally in battle.party_list:
            if ally.alive:
                available_targets.append(ally)

        return random.choice(available_targets)

    def defend(self):
        from Game import battle
        battle.pass_available = False
        self.defending = True
        battle.next_turn()

    def use_spell(self, spell: DamageSpell, target):
        print(self.name + " used " + spell.name + ", it's very effective!")        

        from Game import battle
        import Utilities
        

        offset = 60
        if self.is_enemy:
            offset = offset * -1
            
        if isinstance(spell, DamageSpell) and spell.damage_type == DamageType.PHYSICAL:
            attack_animation_speed = 30        

            Utilities.animate(self.sprite, self.x + offset, self.y, self.x, self.y, self.scale, attack_animation_speed)
            self.attack_timer = attack_animation_speed
            damage_bonus = self.strength
            self.hp -= spell.cost
        else:
            damage_bonus = self.magic_strength
            self.mana -= spell.cost
        battle.pass_available = False
        spell.use(damage_bonus, target, self)

        battle.next_turn()

    def heal(self, amount):
        from Game import battle
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
            
        if not self.alive:
            battle.party_list.insert(self.party_index, self)
            battle.initiative.insert(self.initiative_index, self)
        self.alive = True
        
    def restore_mana(self, amount):
        self.mana += amount
        if self.mana > self.max_mana:
            self.mana = self.max_mana

    def die(self):
        from Game import battle
        import Utilities
        Utilities.animate("Attacks/Death.png", self.x, self.y, self.x, self.y, 3.5)
        self.alive = False
        if self.is_enemy:
            battle.enemy_list.remove(self)
            battle.initiative.remove(self)
        else:
            self.initiative_index = battle.initiative.index(self)
            self.party_index = battle.party_list.index(self)
            if self in battle.available_passes:
                battle.available_passes.remove(self)
            battle.party_list.remove(self)
            battle.initiative.remove(self)
            battle.dead_party_list.append(self)

    def start_turn(self):
        from Game import battle
        self.downed = False
        self.defending = False
        
    def end_turn(self):
        pass
    
    def scale_stats(self, difficulty):
        import math
        harder_more = math.ceil(2 / difficulty)
        harder_less = difficulty - 1
        
        if self.is_enemy:
            random_count = random.randint(1, harder_more)
        else:
            random_count = difficulty - 1
        for i in range(random_count):
            self.weaknesses.append(random.choice(list(DamageType)))
            
        if self.is_enemy:
            random_count = random.randint(1, harder_more)
        else:
            random_count = harder_less
            
        for i in range(random_count):
            damage_type = random.choice(list(DamageType))
            if damage_type not in self.weaknesses:
                self.resists.append(damage_type)
                
        random_count = random.randint(0,2)
        if random_count == 1:
            damage_type = random.choice(list(DamageType))
            if damage_type not in self.weaknesses:
                self.nullifies.append(damage_type)
        if random_count == 2:
            damage_type = random.choice(list(DamageType))
            if damage_type not in self.weaknesses:
                self.drains.append(damage_type)
        multiplier = 7
        self.max_hp *= multiplier * difficulty - multiplier + 1
        self.max_mana *= multiplier * difficulty - multiplier + 1

        self.base_damage *= difficulty
        
        self.hp = self.max_hp
        self.mana = self.max_mana

        self.strength *= difficulty
        self.magic_strength *= difficulty
        self.armor *= difficulty
        self.agility *= difficulty
        self.luck *= difficulty

    def randomize_spells(self, difficulty):
        self.spells = []
        spell_count = random.randint(3, 5)
        
        for i in range(spell_count):
            if difficulty == 1:
                random_spell = spell_dict[random.choice(list(spell_dict))]
            if difficulty == 2:
                random_spell = spell_dict_2[random.choice(list(spell_dict_2))]
            if difficulty == 3:
                random_spell = spell_dict_3[random.choice(list(spell_dict_3))]
            if random_spell in self.spells or (random_spell.name == "Revivify" and self.is_ai):
                i -= 1
                continue
            self.spells.append(random_spell)
            
player_dict = {
    'cloud': {
        "name": "Cloud",
        "sprite": "cloud.png",
        "scale": 0.5,
        "max_hp": 30,
        "max_mana": 16,
        "base_damage": 8,
        "strength": 10,
        "magic_strength": 15,
        "armor": 12,
        "agility": 20,
        "luck": 12,
        "spells": [spell_dict['electro_1'], spell_dict['multi_electro_1'], spell_dict['heal_1'], spell_dict['revive_1']],
        "weaknesses": [DamageType.WIND],
        'resists': [DamageType.ELECTRIC],
        'nullifies': [],
        'drains': [],
        "is_ai": False,
    },
    'joker': {
        "name": "Joker",
        "sprite": "Joker.png",
        "scale": 1.25,
        "max_hp": 30,
        "max_mana": 16,
        "base_damage": 8,
        "strength": 12,
        "magic_strength": 14,
        "armor": 10,
        "agility": 20,
        "luck": 12,
        "spells": [spell_dict['curse_1'], spell_dict['multi_heal_1'], spell_dict['revive_1']],
        "weaknesses": [DamageType.BLESS],
        'resists': [DamageType.CURSE],
        'nullifies': [],
        'drains': [],
        "is_ai": False,
    },
    'barbarian': {
        "name": "Barbarian",
        "sprite": "Barbarian.png",
        "scale": 2.5,
        "max_hp": 35,
        "max_mana": 8,
        "base_damage": 12,
        "strength": 15,
        "magic_strength": 8,
        "armor": 15,
        "agility": 10,
        "luck": 12,
        "spells": [spell_dict['fire_1'], spell_dict['phys_1']],
        "weaknesses": [DamageType.ICE],
        'resists': [DamageType.FIRE],
        'nullifies': [],
        'drains': [],
        "is_ai": False,
    },
}

enemy_dict = {
    "slime": {
        "name": "Slime",
        "sprite": "slime.png",
        "scale": 1,
        "max_hp": 40,
        "max_mana": 1000,
        "base_damage": 6,
        "strength": 5,
        "magic_strength": 10,
        "armor": 10,
        "agility": 10,
        "luck": 10,
        "spells": [spell_dict['psychic_1'], spell_dict['multi_fire_1']],
        "weaknesses": [DamageType.WIND],
        'resists': [],
        'nullifies': [],
        'drains': [],
        "is_ai": True,
    },
    "pixie": {
        "name": "Pixie",
        "sprite": "Pixie.png",
        "scale": 1.25,
        "max_hp": 30,
        "max_mana": 1000,
        "base_damage": 6,
        "strength": 5,
        "magic_strength": 10,
        "armor": 10,
        "agility": 10,
        "luck": 10,
        "spells": [spell_dict['fire_1'], spell_dict['heal_1'], spell_dict['multi_heal_1']],
        "weaknesses": [DamageType.ICE, DamageType.CURSE],
        'resists': [],
        'nullifies': [],
        'drains': [],
        "is_ai": True,
    },
    "jack_frost": {
        "name": "Jack Frost",
        "sprite": "Jack Frost.png",
        "scale": 2.5,
        "max_hp": 50,
        "max_mana": 1000,
        "base_damage": 6,
        "strength": 5,
        "magic_strength": 10,
        "armor": 10,
        "agility": 10,
        "luck": 10,
        "spells": [spell_dict['ice_1'], spell_dict['multi_ice_1']],
        "weaknesses": [DamageType.FIRE],
        'resists': [],
        'nullifies': [],
        'drains': [],
        "is_ai": True,
    }, 
    'pyro_jack': {
        "name": "Pyro Jack",
        "sprite": "Pyro Jack.png",
        "scale": 1,
        "max_hp": 35,
        "max_mana": 16,
        "base_damage": 7,
        "strength": 12,
        "magic_strength": 10,
        "armor": 12,
        "agility": 10,
        "luck": 12,
        "spells": [spell_dict['electro_1'], spell_dict['multi_electro_1'], spell_dict['heal_1'], spell_dict['revive_1']],
        "weaknesses": [DamageType.WIND],
        'resists': [DamageType.ELECTRIC],
        'nullifies': [],
        'drains': [],
        "is_ai": True,
    }
}