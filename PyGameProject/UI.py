import pygame

def draw_chevron():
    from Game import screen
    from Game import initiative
    from Game import turn
    tempImg = pygame.image.load('chevron.png')
    tempImg = pygame.transform.scale_by(tempImg, 0.05)
    tempRect = tempImg.get_rect()
    tempRect.center = (initiative[turn].x, 100)
    screen.blit(tempImg, tempRect)
    
def draw_text(text, font, text_col, x, y):
    from Game import screen
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))