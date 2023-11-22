import random
import pygame
import UI
import sys
pygame.init()

class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0
        
        self.append_option('Play', self.open_play_menu)
        self.append_option('Quit', quit)

    def append_option(self, option, callback):
        self._option_surfaces.append(UI.font_big.render(option, True, UI.WHITE))
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) -1))

    def open_play_menu(self):
        import Game
        Game.menu = PlayMenu()

    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        from Game import screen, screenHeight, screenWidth, panelHeight
        image = pygame.image.load('menu bg.png')
        UI.draw_bg(image)
        UI.draw_text('Super Mega Hyper', UI.font_bigger, UI.WHITE, screenWidth / 2, 100)
        UI.draw_text('Combat X', UI.font_bigger, UI.WHITE, screenWidth / 2, 180)
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.center = (x / 2, y / 2 + i * option_y_padding)
            if i == self._current_option_index:
                pygame.draw.rect(surf, (0,100,0), option_rect)
            surf.blit(option, option_rect)
            
    def update(self):
        from Game import screen, screenHeight, screenWidth, panelHeight
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.switch(-1)
                if event.key == pygame.K_DOWN:
                    self.switch(1)
                if event.key == pygame.K_z:
                    self.select()
        self.draw(screen, screenWidth, screenHeight + panelHeight + 50, 100)
        
    
class PlayMenu(Menu):
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0
        
        self.append_option('Easy', self.easy)
        self.append_option('Medium', self.medium)
        self.append_option('Hard', self.hard)
        
    def draw(self, surf, x, y, option_y_padding):
        from Game import screen, screenHeight, screenWidth, panelHeight
        image = pygame.image.load('menu bg.png')
        UI.draw_bg(image)
        UI.draw_text('Choose Difficulty', UI.font_bigger, UI.WHITE, screenWidth / 2, 100)
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.center = (x / 2, y / 2 + i * option_y_padding)
            if i == self._current_option_index:
                pygame.draw.rect(surf, (0,100,0), option_rect)
            surf.blit(option, option_rect)
          
    def easy(self):
        self.start_game(1)
        
    def medium(self):
        self.start_game(2)
        
    def hard(self):
        self.start_game(3)
        
    def start_game(self, difficulty = 1):
        from Battle import Battle
        from Character import Character, player_dict, enemy_dict
        import Game
        
        #player_count = random.randint(1, 3)
        player_list = [player_dict['cloud'], player_dict['joker'], player_dict['barbarian']]
        #for i in range(0, player_count):
        #    player_list.append(player_dict[random.choice(list(player_dict))])
            
        enemy_list = []
        for i in range(0, difficulty + 2):
            enemy_list.append(enemy_dict[random.choice(list(enemy_dict))])

        Game.battle = Battle(allies=player_list, enemies=enemy_list, difficulty=difficulty)
        Game.menu = None