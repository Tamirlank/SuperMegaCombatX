import pygame
import sys
import os
from Character import Character 
import UI
import random
from Spells import DamageSpell, DamageType, HealingSpell, spell_dict
from Utilities import *

# Main script
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

bg = pygame.image.load(os.path.join("./background.png"))
bg = pygame.transform.scale(bg, (screenWidth, screenHeight))

pygame.display.set_caption('Super Ultra Hyper Mega Combat X')


cloud = Character('Cloud', sprite='cloud.png', scale=0.5, 
                  max_hp=30, max_mana=10, spells=[spell_dict['fire_1'], spell_dict['multi_fire_1'], spell_dict['multi_heal_1']],
                  strength=10, magic_strength=10, armor=10, agility=10, luck=10,
                  is_enemy=False, is_ai=False)

cloud2 = Character('Barbarian', sprite='Barbarian.png', scale=0.5,
                  max_hp=35, max_mana=6, spells=[spell_dict["electro_1"], spell_dict["heal_1"]],
                  strength=20, magic_strength=6, armor=15, agility=10, luck=10,
                  is_enemy=False, is_ai=False)

slime = Character('Slime', sprite='slime.png', scale=0.15, is_enemy=True, 
                max_hp=30, max_mana=10,
                strength=5, magic_strength=10, armor=10, agility=10, luck=10)
slime2 = Character('Slime', sprite='slime.png', scale=0.15, is_enemy=True, 
                max_hp=30, max_mana=10,
                strength=5, magic_strength=10, armor=10, agility=10, luck=10)
slime3 = Character('Slime', sprite='slime.png', scale=0.15, is_enemy=True, 
                max_hp=30, max_mana=10,
                strength=5, magic_strength=10, armor=10, agility=10, luck=10)

random.shuffle(initiative)
current_turn = 0
current_character: Character = initiative[0]
highlited_spell = 0
selected_spell = None
choosing_spell = False
targeting_teammates = False
selected_teammate = 0
target: Character

# Functions
def render_frame():
    global current_character, choosing_spell, selected_spell
    UI.draw_bg()
    pygame.draw.rect(screen, (0,0,0), (0, screenHeight, screenWidth, panelHeight))
    pygame.draw.line(screen, UI.WHITE, (0, screenHeight), (screenWidth, screenHeight), 2)
    UI.draw_characters()
    if (current_character in party_list):
        if choosing_spell:
            UI.draw_spells()
        else:
            UI.draw_controls()
            UI.draw_party_health()
            if selected_spell is not None and selected_spell.multi_target:
                UI.draw_chevron_all()
            else:
                UI.draw_chevron()
    else:
        UI.draw_party_health()
            
def next_turn():
    global current_turn
    global turn_timer
    global initiative

    turn_timer = time_between_turns
    current_turn += 1
    if (current_turn > len(initiative) - 1):
            current_turn = 0

    initiative[current_turn].start_turn()
    
def skip_turn():
    global current_turn
    global initiative

    current_turn += 1
    if (current_turn > len(initiative) - 1):
            current_turn = 0

    initiative[current_turn].start_turn()
def manage_turn():
    global turn_timer
    global current_turn
    global initiative
    global current_character
    
    current_character = initiative[current_turn]
    turn_timer -= 1
    if (turn_timer > 0):
        return


    if (current_character not in party_list):
        if (current_character.alive != True):
            initiative.remove(current_character)
            enemy_list.remove(current_character)
            return

        current_character.random_attack()
        
def input_manager():
    global turn_timer, current_turn, selectedEnemy, initiative, current_character
    global choosing_spell, casting_spell, selected_spell, highlited_spell, targeting_teammates, selected_teammate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if current_character not in party_list or not enemy_list or not party_list:
                return
            if choosing_spell:
                # Spell Selector
                if event.key == pygame.K_LEFT:
                    highlited_spell -= 1
                if event.key == pygame.K_RIGHT:
                    highlited_spell += 1
                if event.key == pygame.K_UP:
                    highlited_spell -= 4
                if event.key == pygame.K_DOWN:
                    highlited_spell += 4
                if highlited_spell >= len(current_character.spells):
                    highlited_spell = len(current_character.spells) - 1
                elif highlited_spell <= -1:
                    highlited_spell = 0
                    
                if event.key == pygame.K_x:
                    choosing_spell = False
                    selected_spell = None

                if event.key == pygame.K_z:
                    if current_character.mana < current_character.spells[highlited_spell].cost: return
                    
                    selected_spell = current_character.spells[highlited_spell]
                    if type(selected_spell) == DamageSpell:
                        targeting_teammates = False
                    elif type(selected_spell) == HealingSpell:
                        targeting_teammates = True
                    choosing_spell = False
                return
        #----------------------------------------------------        
        # Choosing Target
            if not targeting_teammates:
                if event.key == pygame.K_LEFT:
                    selectedEnemy -= 1
                if event.key == pygame.K_RIGHT:
                    selectedEnemy += 1
                selectedEnemy = clamp_number_loop(selectedEnemy, 0, len(enemy_list) - 1)
                selected_teammate = clamp_number_loop(selected_teammate, 0, len(party_list) - 1)
                target = enemy_list[selectedEnemy]
            else:
                if event.key == pygame.K_LEFT:
                    selected_teammate -= 1
                if event.key == pygame.K_RIGHT:
                    selected_teammate += 1
                selectedEnemy = clamp_number_loop(selectedEnemy, 0, len(enemy_list) - 1)
                selected_teammate = clamp_number_loop(selected_teammate, 0, len(party_list) - 1)
                target = party_list[selected_teammate]
            if event.key == pygame.K_z:
                if selected_spell == None:
                    current_character.attack(target)
                else:
                    current_character.use_spell(selected_spell, target)
                    selected_spell = None
                    targeting_teammates = False
                turn_timer = time_between_turns
                    
            if event.key == pygame.K_x:
                choosing_spell = True
                    
            if event.key == pygame.K_v:
                current_character.defend()

initiative[0].start_turn()


def display_data(enemy_list, party_list):
    if not enemy_list:
        # Если список пуст, отображаем изображение
        show_image("win.png")
    if not party_list:
        # Если список не пуст, отображаем информацию
        show_image("loss.png")

def show_image(image_path):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (screenWidth, screenHeight + panelHeight))
    screen.blit(image, (0, 0))


# Update Loop
while True:
    clock.tick(60)
    selectedEnemy = clamp_number_loop(selectedEnemy, 0, len(enemy_list) - 1)
    selected_teammate = clamp_number_loop(selected_teammate, 0, len(party_list) - 1)
    #render stuff
    render_frame()

    manage_turn()
    
    #close the game if it's... closed
    input_manager()

    display_data(enemy_list, party_list)

    #update game state
    pygame.display.update()
