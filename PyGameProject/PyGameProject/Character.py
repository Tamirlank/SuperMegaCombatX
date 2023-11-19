import pygame
from Spells import DamageType, spell_dict, DamageSpell

class Character():
    weakness_list: DamageType = []
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
    
    is_enemy: bool=None 
    add_to_initiative: bool=True 
    is_ai: bool=True
    
    def __init__(self, name: str,sprite: str, scale: float, 
                 max_hp: int, max_mana: int, base_damage: int,
                 strength: int, magic_strength: int, armor: int, agility: int, luck: int,
                 spells: DamageSpell = [], weaknesses: DamageType = [],
                 is_enemy: bool=None, add_to_initiative: bool=True, is_ai: bool=True):
        
        from Game import initiative, enemy_list, party_list
        self.x = 0
        self.y = 225
        self.raised_y = self.y - 25
    
        self.spells = spells

        self.name = name
        
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mana = max_mana
        self.mana = max_mana
        
        self.base_damage = base_damage
        
        self.strength = strength
        self.magic_strength = magic_strength
        self.armor = armor
        self.agility = agility
        self.luck = luck
        
        self.alive = True
        
        self.defending = False
        
        self.is_enemy = is_enemy
        self.is_ai = is_ai

        self.sprite = sprite
        self.scale = scale

        if add_to_initiative:
            if is_enemy==None:
                print("Character not specified as enemy or teammate, did not add to initiative")
                return
            initiative.append(self)
            
            if is_enemy:
                enemy_list.append(self)
                for character in initiative:
                    character.x = 0
                    character.refactor_position()
            else:
                party_list.append(self)
                for character in initiative:
                    character.x = 0
                    character.refactor_position()
                
        
        self.image = pygame.image.load(sprite)
        self.image = pygame.transform.scale_by(self.image, scale)
        self.rect = self.image.get_rect()

    def refactor_position(self):
        from Game import screenWidth, enemy_list, party_list
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

    def draw(self):
        from Game import screen, initiative, current_turn
        if initiative[current_turn] == self:
            self.rect.center = (self.x, self.raised_y)
        else:
            self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)
        #pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 30)

    def take_damage(self, damage: int, type: DamageType = 0):
        damage_amount = damage
        if self.defending:
            damage_amount = damage_amount // 2
            
        amount = round(float(damage_amount) * (1 - float(self.armor) / 200))

        self.hp -= amount
        if (self.hp <= 0):
            self.hp = 0
            self.die()
        
    def attack(self, target):
        from Game import next_turn
        target.take_damage(self.base_damage + round(self.base_damage * float(self.strength) / 100))
        next_turn()

    def random_attack(self):
        from Game import next_turn, party_list, enemy_list
        import random
        
                
        if self.is_enemy:
            index_list = []
            for i in range(len(party_list)):
                if party_list[i].alive:
                    index_list.append(i)
                    
            random_target_index = random.randint(0, len(index_list)-1)
            target = party_list[index_list[random_target_index]]
        else:
            random_target_index = random.randint(0, len(enemy_list)-1)
            target = enemy_list[random_target_index]
        self.attack(target)

    def defend(self):
        from Game import next_turn
        self.defending = True
        next_turn()
        
    def use_spell(self, spell: DamageSpell, target):
        from Game import next_turn

        if isinstance(spell, DamageSpell) and spell.damage_type == DamageType.PHYSICAL:
            damage_bonus = self.strength
            self.hp -= spell.cost
        else:
            damage_bonus = self.magic_strength
            self.mana -= spell.cost

        spell.use(damage_bonus, target)
        
        next_turn()

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        self.alive = True

    def die(self):
        from Game import enemy_list, initiative, party_list
        self.alive = False
        if (self.is_enemy):
            enemy_list.remove(self)
            initiative.remove(self)

    def start_turn(self):
        from Game import skip_turn
            
        self.defending = False
        if not self.alive:
            skip_turn()
            return