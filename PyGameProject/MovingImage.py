import pygame
from Utilities import *
import UI
pygame.init()

class MovingImage():
    def __init__(self, image_path, start_x, start_y, end_x, end_y, scale, duration: int = 30):
        from Game import clock
        self.image_path = image_path
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.duration = duration
        self.timer = duration
        if not image_path:
            return

        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale_by(self.image, scale)
        
    def image_animation(self):
        if not self.image_path:
            return
        
        from Game import screen, moving_images
        
        
        self.timer -= 1
        
        progress = 1 - self.timer / self.duration
        
        x = lerp(self.start_x, self.end_x, progress)
        y = lerp(self.start_y, self.end_y, progress)

        image_rect = self.image.get_rect()
        image_rect.center = (x, y)
        screen.blit(self.image, image_rect)
        
        if self.timer <= 0:
            moving_images.remove(self)
            
def animate(sprite, origin_x, origin_y, target_x, target_y, sprite_scale, duration: int = 30):
    from Game import moving_images
    moving_images.append(MovingImage(sprite, origin_x, origin_y, target_x, target_y, sprite_scale, duration))