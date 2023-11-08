import pygame
from Spell import DamageType, spell_list, Spell

class Character():
    weakness_list = []
    def __init__(self, x: float, y: float, name: str, max_hp: int, strength: int, sprite: str, scale: float, is_enemy: bool=None, add_to_initiative: bool=True, is_ai: bool=True):
        from Game import initiative, enemy_list, party_list
        self.x = x
        self.y = y
        self.raised_y = y + 25
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.alive = True
        self.image = pygame.image.load(sprite)
        self.image = pygame.transform.scale_by(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.defending = False
        self.is_enemy = is_enemy
        self.is_ai = is_ai
        if add_to_initiative:
            if is_enemy==None:
                print("Character not specified as enemy or teammate, did not add to initiative")
                return
            initiative.append(self)
            if is_enemy:
                enemy_list.append(self)
            else:
                party_list.append(self)

        # self.spells = spells
        #self.image = pygame.transform.scale_by(self.image, )
        
    def draw(self):
        from Game import screen, initiative, current_turn
        if initiative[current_turn] == self:
            self.rect.center = (self.x, self.raised_y)
        else:
            self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)
        #pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 30)

    def take_damage(self, damage_amount, type: DamageType = 0):
        amount = damage_amount
        if self.defending:
            amount = damage_amount // 2
        self.hp -= amount
        if (self.hp < 0):
            self.hp = 0
            self.alive = False
        
    def attack(self, target):
        from Game import next_turn
        target.take_damage(self.strength)
        next_turn()

    def random_attack(self):
        from Game import next_turn, party_list, enemy_list
        import random
        if self.is_enemy:
            random_target_index = random.randint(0, len(party_list)-1)
            target = party_list[random_target_index]
        else:
            random_target_index = random.randint(0, len(enemy_list)-1)
            target = enemy_list[random_target_index]
        target.take_damage(self.strength)
        next_turn()

    def defend(self):
        from Game import next_turn
        self.defending = True
        next_turn()
        
    def magic_attack(self, spell: Spell, target):
        if (spell.multi_target):
            from Game import enemy_list
            for enemy in enemy_list:
                enemy.take_damage(spell.base_damage)
        target.take_damage(spell.base_damage)


    def start_turn(self):
        from Game import next_turn
        self.defending = False
        if not self.alive:
            next_turn()
            return