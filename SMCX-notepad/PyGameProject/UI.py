import select
import pygame
from Utilities import *
from Character import Character

pygame.init()

RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont('Arial', 26)

def draw_bg():
    from Game import screen, bg
    screen.blit(bg, (0, 0))

def draw_characters():
    from Game import initiative
    for character in initiative:
        character.draw()
        
def draw_party_health():
    from Game import party_list, screenHeight
    y = 50
    for character in party_list:
        draw_text(f'{character.name} HP: {character.hp} Mana: {character.mana}', font, GREEN, 200, screenHeight + y)
        draw_healthbar(character, 700, screenHeight + y, 150, 20)
        y += 30
        
def draw_spells():
    from Game import current_character, screenWidth, screenHeight, panelHeight, highlited_spell
    horizontal_spacing = screenWidth / 5
    vertical_spacing = panelHeight / 3

    i = 1
    j = 1

    k = 0
    for spell in current_character.spells:
        color = WHITE
        if highlited_spell == k:
            color = GREEN
            if current_character.mana < current_character.spells[highlited_spell].cost:
                color = RED
        draw_text(spell.name, font, color, horizontal_spacing * i, screenHeight + vertical_spacing * j - 15)
        draw_text(f'Mana Cost: {spell.cost}', font, color, horizontal_spacing * i, screenHeight + vertical_spacing * j + 15)
        i += 1
        k += 1
        if (i == 5):
            i = 1
            j = 2
            
def draw_chevron():
    from Game import screen, enemy_list, selectedEnemy, targeting_teammates, party_list, selected_teammate
    

    if not enemy_list or not party_list:
        return
        
    target: Character
    try:
        if not targeting_teammates:
            target = enemy_list[selectedEnemy]
        else:
            target = party_list[selected_teammate]
    except:
        return
    temp_img = pygame.image.load('chevron.png')
    temp_img = pygame.transform.scale_by(temp_img, 0.05)
    temp_rect = temp_img.get_rect()
    temp_rect.center = (target.x, target.y - 100)
    screen.blit(temp_img, temp_rect)
    draw_text(f'{target.name} HP: {target.hp}', font, RED, target.x, target.y + 80)
    draw_healthbar(target, target.x, target.y + 110, 150, 20)

def draw_chevron_all():
    from Game import screen, enemy_list, targeting_teammates, party_list
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
    from Game import screenHeight, panelHeight
    
    draw_text('Z: Attack', font, WHITE, 200, screenHeight + panelHeight - 20)
    draw_text('X: Spell', font, WHITE, 350, screenHeight + panelHeight - 20)
    draw_text('C: Item', font, WHITE, 500, screenHeight + panelHeight - 20)
    draw_text('V: Shield', font, WHITE, 650, screenHeight + panelHeight - 20)
    #draw_text('Shift: Baton Pass', font, WHITE, 200, screenHeight + panelHeight - 60)