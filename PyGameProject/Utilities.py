import pygame

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
    


def clamp_number(num, a, b):
    if num < a:
        num = a
    elif num > b:
        num = b
    return num

def clamp_number_loop(num, a, b):
    if num > b:
        num = a
    elif num < a:
        num = b
    return num

def lerp(a, b, t):
    return a + (b - a) * t

def rot_center(image, angle, x, y):
    import pygame
    pygame.init()
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect