import pygame
import sys
import os
from Character import Character 
import UI

pygame.init()
clock = pygame.time.Clock()

screenWidth = 960
screenHeight = 540

screen = pygame.display.set_mode((screenWidth, screenHeight + 150))

font = pygame.font.SysFont('Arial', 26)

red = (255, 0, 0)
green = (0, 255, 0)

bg = pygame.image.load(os.path.join("./", "background.png"))
bg = pygame.transform.scale(bg, (screenWidth, screenHeight))

pygame.display.set_caption('Super Combat X')

cloud = Character(200, 250, 'Cloud', 30, 10, 'cloud.jpg', 0.5)
slime = Character(700, 250, 'Slime', 30, 10, 'Slime.png', 0.25)

initiative = [cloud, slime]
turn = 0

# Functions

def draw_bg():
    screen.blit(bg, (0, 0))

def draw_characters():
    cloud.draw()
    slime.draw()

# Update Loop

while True:
    clock.tick(60)
    x, y = pygame.mouse.get_pos()

    #render stuff
    draw_bg()
    draw_characters()
    UI.draw_chevron()
    
    UI.draw_text(f'{cloud.name} HP: {cloud.hp}', font, green, 200, 120)

    #close the game if it's... closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                turn += 1
                if (turn > len(initiative) - 1):
                    turn = 0

    #update game state
    pygame.display.update()