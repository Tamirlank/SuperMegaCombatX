import pygame
from Spell import DamageType, spell_list, Spell

class Character():
    weakness_list = []
    def __init__(self, x: float, y: float, name: str, max_hp: int, strength: int, sprite: str, scale: float, spells):
        self.x = x
        self.y = y
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.alive = True
        self.image = pygame.image.load(sprite)
        self.image = pygame.transform.scale_by(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.spells = spells
        #self.image = pygame.transform.scale_by(self.image, )
        
    def draw(self):
        from Game import screen
        screen.blit(self.image, self.rect)
        #pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 30)
    
    def take_damage(self, amount, type: DamageType = 0):
        self.hp -= amount
        if (self.hp < 0):
            self.hp = 0
            self.alive = False
        
    def attack(self, target):
        target.take_damage(self.strength)
        
    def magic_attack(self, spell: Spell, target):
        if (spell.multi_target):
            from Game import enemy_list
            for enemy in enemy_list:
                enemy.take_damage(spell.base_damage)
        target.take_damage(spell.base_damage)