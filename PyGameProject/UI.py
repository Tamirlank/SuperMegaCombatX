import pygame
import Game

def draw_chevron():
    tempImg = pygame.image.load('chevron.png')
    tempImg = pygame.transform.scale_by(tempImg, 0.05)
    tempRect = tempImg.get_rect()
    tempRect.center = (Game.initiative[Game.turn].x, 100)
    Game.screen.blit(tempImg, tempRect)
    
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    Game.screen.blit(img, (x, y))