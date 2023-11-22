from Battle import Battle
from Menu import Menu
from Character import Character, enemy_dict, player_dict
import sys
import pygame
import json

pygame.init()

clock = pygame.time.Clock()

screenWidth = 1200
screenHeight = 400
panelHeight = 250
screen = pygame.display.set_mode((screenWidth, screenHeight + panelHeight))

pygame.display.set_caption('Super Ultra Hyper Mega Combat X')
menu = Menu()
battle: Battle = None



moving_images = []

while True:
    clock.tick(60)
    if menu is not None:
        menu.update()
    if battle is not None:
        battle.update()
    for i in moving_images:
        i.image_animation()
    pygame.display.update()