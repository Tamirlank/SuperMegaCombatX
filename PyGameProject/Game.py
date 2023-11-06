import pygame
import sys
import os
from Character import Character 
import UI
import random
from Spell import Spell, DamageType

time_between_turns = 30
turn_timer = 30

pygame.init()
clock = pygame.time.Clock()

screenWidth = 900
screenHeight = 400
panelHeight = 200

screen = pygame.display.set_mode((screenWidth, screenHeight + panelHeight))

RED = (255, 0, 0)
GREEN = (0, 255, 0)

bg = pygame.image.load(os.path.join("./", "background.png"))
bg = pygame.transform.scale(bg, (screenWidth, screenHeight))

pygame.display.set_caption('Super Combat X')

cloud = Character(200, 225, 'Cloud', 30, 10, 'cloud.png', 0.40)
slime1 = Character(550, 200, 'Slime', 30, 5, 'slime.png', 0.10)
slime2 = Character(650, 225, 'Slime', 30, 5, 'slime.png', 0.10)
slime3 = Character(750, 200, 'Slime', 30, 5, 'slime.png', 0.10)

selectedEnemy = 0
enemy_list = []
enemy_list.append(slime1)
enemy_list.append(slime2)
enemy_list.append(slime3)

initiative = []
for enemy in enemy_list:
    initiative.append(enemy)
initiative.append(cloud)
random.shuffle(initiative)
current_turn = 0

# Functions
def draw_bg():
    screen.blit(bg, (0, 0))

def draw_characters():
    cloud.draw()
    slime1.draw()
    slime2.draw()
    slime3.draw()
    
def render_frame():
    draw_bg()
    pygame.draw.rect(screen, (0,0,0), (0, screenHeight, screenWidth, panelHeight))
    draw_characters()
    UI.draw_controls()

    if (initiative[current_turn] == cloud):
        UI.draw_chevron()
    
    UI.draw_text(f'{cloud.name} HP: {cloud.hp}', UI.font, GREEN, 200, screenHeight + 50)
    
def manage_turn():
    global turn_timer
    global current_turn

    turn_timer -= 1
    if (turn_timer > 0):
        return
    
    if (initiative[current_turn] != cloud):
        current_character = initiative[current_turn]
        
        if (current_character.alive != True):
            initiative.remove(current_character)
            enemy_list.remove(current_character)
            return
        
        current_character.attack(cloud)
        current_turn += 1
        
        if (current_turn > len(initiative) - 1):
            current_turn = 0
            
        turn_timer = time_between_turns
            
def input_manager():
    global turn_timer
    global current_turn
    global selectedEnemy

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                selectedEnemy -= 1
                if (selectedEnemy < 0):
                    selectedEnemy = len(enemy_list) -1
                    
            if event.key == pygame.K_RIGHT:
                selectedEnemy += 1
                if (selectedEnemy > len(enemy_list) - 1):
                    selectedEnemy = 0
                    
            if event.key == pygame.K_z:
                cloud.attack(enemy_list[selectedEnemy])
                current_turn += 1
                turn_timer = time_between_turns
                if (current_turn > len(initiative) - 1):
                    current_turn = 0
    

# Update Loop
while True:
    clock.tick(60)

    #render stuff
    render_frame()

    manage_turn()

    #close the game if it's... closed
    input_manager()
    
    #update game state
    pygame.display.update()