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