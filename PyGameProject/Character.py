import pygame
class Character():
    weakness_list = []
    def __init__(self, x, y, name, max_hp, strength, sprite, scale):
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
        #self.image = pygame.transform.scale_by(self.image, )
        
    def draw(self):
        from Game import screen
        screen.blit(self.image, self.rect)
        #pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 30)
    
    def take_damage(self, amount):
        self.hp -= amount
        if (self.hp < 0):
            self.hp = 0
            self.alive = False
        
    def attack(self, target):
        target.take_damage(self.strength)