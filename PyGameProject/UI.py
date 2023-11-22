import select
import string
from Spells import HealingSpell
from Utilities import *
from Character import Character
import pygame

pygame.init()

RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont('Arial', 26)
font_big = pygame.font.SysFont('arial', 60)
font_bigger = pygame.font.SysFont('arial', 80)

cutin_timer = 0

def draw_bg(bg):
    from Game import screen
    screen.blit(bg, (0, 0))

def draw_characters(initiative, current_character):
    for character in initiative:
        character.draw(initiative, current_character)
        
def draw_party_health(party_list):
    from Game import screenHeight, battle, screenWidth
    y = 50
    for character in party_list:
        draw_text(f'{character.name} HP: {character.hp} Mana: {character.mana}', font, GREEN, screenWidth / 4, screenHeight + y)
        draw_healthbar(character, screenWidth / 4 * 3, screenHeight + y, 150, 20)
        y += 30
        
crit_image = pygame.image.load('Crit Cut In.png')
crit_image = pygame.transform.scale_by(crit_image, 8)
crit_rect = crit_image.get_rect()
    
def draw_cut_in():
    from Game import screen, screenHeight, screenWidth
    global cutin_timer, crit_image, crit_rect
    if cutin_timer <= 0:
        return
    cutin_timer -= 1
    crit_rect.center = (screenWidth / 2, screenHeight / 2)
    screen.blit(crit_image, crit_rect)

def draw_spells(current_character, highlited_menu_item):
    from Game import screenWidth, screenHeight, panelHeight
    from Spells import DamageType, DamageSpell
    horizontal_spacing = screenWidth / 5
    vertical_spacing = panelHeight / 3

    i = 1
    j = 1

    k = 0
    for spell in current_character.spells:
        color = WHITE
        
        if isinstance(spell, DamageSpell) and spell.damage_type == DamageType.PHYSICAL:
            cost_text = f'HP Cost: {spell.cost}'
        else:
            cost_text = f'Mana Cost: {spell.cost}'
            
        if highlited_menu_item == k:
            color = GREEN
            
            temp_spell = current_character.spells[highlited_menu_item]
        
            if isinstance(temp_spell, DamageSpell) and temp_spell.damage_type == DamageType.PHYSICAL:
                if current_character.hp <= temp_spell.cost: 
                    color = RED
            else:
                if current_character.mana < temp_spell.cost:
                    color = RED
                    

        draw_text(spell.name, font, color, horizontal_spacing * i, screenHeight + vertical_spacing * j - 15)
        draw_text(cost_text, font, color, horizontal_spacing * i, screenHeight + vertical_spacing * j + 15)
        i += 1
        k += 1
        if (i == 5):
            i = 1
            j = 2
            
def draw_chevron():
    from Game import screen, battle
    if not battle.enemy_list or not battle.party_list:
        return
    target = battle.target
    temp_img = pygame.image.load('chevron.png')
    temp_img = pygame.transform.scale_by(temp_img, 0.05)
    temp_rect = temp_img.get_rect()
    temp_rect.center = (target.x, target.y - 100)
    screen.blit(temp_img, temp_rect)
    draw_text(f'{target.name} HP: {target.hp}', font, RED, target.x, target.y + 80)
    draw_healthbar(target, target.x, target.y + 110, 150, 20)

def draw_chevron_all(enemy_list, targeting_teammates, party_list):
    from Game import screen
    if targeting_teammates:
        for target in party_list:
            temp_img = pygame.image.load('chevron.png')
            temp_img = pygame.transform.scale_by(temp_img, 0.05)
            temp_rect = temp_img.get_rect()
            temp_rect.center = (target.x, target.y - 100)
            screen.blit(temp_img, temp_rect)
            draw_healthbar(target, target.x, target.y + 110, 50, 20)
    else: 
        for target in enemy_list:
            temp_img = pygame.image.load('chevron.png')
            temp_img = pygame.transform.scale_by(temp_img, 0.05)
            temp_rect = temp_img.get_rect()
            temp_rect.center = (target.x, target.y - 100)
            screen.blit(temp_img, temp_rect)
            draw_healthbar(target, target.x, target.y + 110, 50, 20)

def draw_game_ending(enemy_list, party_list, initiative):
    if not enemy_list:
        draw_image("win.png")
        
    for member in party_list:
        if member.alive:
            return
    draw_image("loss.png")

def draw_image(image_path):
    from Game import screen, screenHeight, screenWidth, panelHeight
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (screenWidth, screenHeight + panelHeight))
    screen.blit(image, (0, 0))
    
def draw_text(text, font, text_col, x, y):
    from Game import screen
    img = font.render(text, True, text_col)
    text_rect = img.get_rect(center=(x, y))
    screen.blit(img, text_rect)
    
def draw_healthbar(character, x, y, width, height):
    from Game import screen
    pygame.draw.rect(screen, RED, (x - width / 2, y - height / 2, width, height))
    pygame.draw.rect(screen, GREEN, (x - width / 2, y - height / 2, width * (character.hp / character.max_hp), height))



def draw_controls():
    from Game import screenHeight, panelHeight, battle, screenWidth
    from Battle import GameState
    if battle.game_state == GameState.IN_MENU:
        draw_text('Z: Select Spell', font, WHITE, screenWidth / 3, screenHeight + panelHeight - 20)
        draw_text('X: Cancel', font, WHITE, screenWidth / 3 * 2, screenHeight + panelHeight - 20)
    elif battle.selected_spell:
        draw_text('Z: Use Spell', font, WHITE, screenWidth / 3, screenHeight + panelHeight - 20)
        draw_text('X: Cancel', font, WHITE, screenWidth / 3 * 2, screenHeight + panelHeight - 20)
    elif battle.game_state == GameState.PASSING_TURN:
        draw_text('Z: Select Teammate', font, WHITE, screenWidth / 3, screenHeight + panelHeight - 20)
        draw_text('B: Cancel', font, WHITE, screenWidth / 3 * 2, screenHeight + panelHeight - 20)
    else:
        slots = 4
        if battle.pass_available and battle.available_passes:
            slots = 5
            draw_text('B: Baton Pass', font, WHITE, screenWidth / slots * 4, screenHeight + panelHeight - 20)
        
        draw_text('Z: Attack', font, WHITE, screenWidth / slots, screenHeight + panelHeight - 20)
        draw_text('X: Spell', font, WHITE, screenWidth / slots * 2, screenHeight + panelHeight - 20)
        draw_text('V: Shield', font, WHITE, screenWidth / slots * 3, screenHeight + panelHeight - 20)
           