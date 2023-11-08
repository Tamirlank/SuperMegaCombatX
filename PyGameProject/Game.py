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

selectedEnemy = 0
enemy_list = []
party_list = []
initiative = []

RED = (255, 0, 0)
GREEN = (0, 255, 0)

bg = pygame.image.load(os.path.join("./", "background.png"))
bg = pygame.transform.scale(bg, (screenWidth, screenHeight))

pygame.display.set_caption('Super Combat X')

cloud = Character(100, 225, 'Cloud', 30, 10, 'cloud.png', 0.40, is_enemy=False, is_ai=False)
not_cloud = Character(200, 250, "Cloud's Twin Brother", 30, 10, 'cloud.png', 0.40, is_enemy=False, is_ai=False)
cloud3 = Character(300, 225, 'Cloud evil twin', 30, 10, 'cloud.png', 0.40, is_enemy=False, is_ai=False)
cloud4 = Character(400, 250, 'THE FOURTH MOTHERFUCKER', 30, 10, 'cloud.png', 0.40, is_enemy=False, is_ai=False)
slime1 = Character(550, 200, 'Slime1', 30, 5, 'slime.png', 0.10, is_enemy=True)
slime2 = Character(650, 225, 'Slime2', 30, 5, 'slime.png', 0.10, is_enemy=True)
slime3 = Character(750, 200, 'Slime3', 30, 5, 'slime.png', 0.10, is_enemy=True)


random.shuffle(initiative)
current_turn = 0

# Functions
def draw_bg():
    screen.blit(bg, (0, 0))

def draw_characters():
    for character in initiative:
        character.draw()
    
def render_frame():
    draw_bg()
    pygame.draw.rect(screen, (0,0,0), (0, screenHeight, screenWidth, panelHeight))
    draw_characters()
    UI.draw_controls()

    if (initiative[current_turn] in party_list):
        UI.draw_chevron()

    x = 50
    for character in party_list:
        UI.draw_text(f'{character.name} HP: {character.hp}', UI.font, GREEN, 200, screenHeight + x)
        x += 30

def next_turn():
    global current_turn
    global turn_timer
    global initiative

    turn_timer = time_between_turns
    current_turn += 1
    if (current_turn > len(initiative) - 1):
            current_turn = 0

    initiative[current_turn].start_turn()

def manage_turn():
    global turn_timer
    global current_turn
    global initiative

    turn_timer -= 1
    if (turn_timer > 0):
        return

    current_character = initiative[current_turn]

    if (current_character not in party_list):
        if (current_character.alive != True):
            initiative.remove(current_character)
            enemy_list.remove(current_character)
            return

        current_character.random_attack()

            
def input_manager():
    global turn_timer
    global current_turn
    global selectedEnemy
    global initiative
    global cloud
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

            if initiative[current_turn] in party_list:
                current_character = initiative[current_turn]
                if event.key == pygame.K_v:
                    current_character.defend()
                if event.key == pygame.K_z:
                    current_character.attack(enemy_list[selectedEnemy])
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