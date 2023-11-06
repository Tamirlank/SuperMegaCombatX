import pygame

pygame.init()

RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont('Arial', 26)

def draw_chevron():
    from Game import screen, enemy_list, selectedEnemy

    current_enemy = enemy_list[selectedEnemy]
    temp_img = pygame.image.load('chevron.png')
    temp_img = pygame.transform.scale_by(temp_img, 0.05)
    temp_rect = temp_img.get_rect()
    temp_rect.center = (current_enemy.x, current_enemy.y - 100)
    screen.blit(temp_img, temp_rect)
    draw_text(f'{current_enemy.name} HP: {current_enemy.hp}', font, RED, current_enemy.x, current_enemy.y + 80)
    draw_healthbar(current_enemy)
    
def draw_text(text, font, text_col, x, y):
    from Game import screen
    img = font.render(text, True, text_col)
    text_rect = img.get_rect(center=(x, y))
    screen.blit(img, text_rect)
    
def draw_healthbar(character):
    from Game import screen
    pygame.draw.rect(screen, RED, (character.x - 75, character.y + 100, 150, 20))
    pygame.draw.rect(screen, GREEN, (character.x - 75, character.y + 100, 150 * (character.hp / character.max_hp), 20))
    
def draw_controls():
    from Game import screenHeight, panelHeight
    
    draw_text('Z: Attack', font, WHITE, 200, screenHeight + panelHeight - 20)
    draw_text('X: Spell', font, WHITE, 350, screenHeight + panelHeight - 20)
    draw_text('C: Item', font, WHITE, 500, screenHeight + panelHeight - 20)
    draw_text('V: Shield', font, WHITE, 650, screenHeight + panelHeight - 20)
    #draw_text('Shift: Baton Pass', font, WHITE, 200, screenHeight + panelHeight - 60)