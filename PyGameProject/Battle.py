from sched import Event
from socket import gethostbyname_ex
import pygame
import sys
import os
import UI
import random
import copy
from Character import Character, enemy_dict, player_dict
from Spells import *
from Utilities import *
pygame.init()

class GameState(Enum):
    DEFAULT = 0,
    WAITING_TURN = 1,
    IN_MENU = 2,
    PASSING_TURN = 3,

class Battle():
    def __init__(self, allies:Character=[], enemies:Character=[], difficulty:int = 1):
        from Game import screenWidth, screenHeight
        self.game_over = False

        self.time_between_turns = 60
        self.turn_timer = 30

        self.pass_available = False

        self.enemy_list = []
        self.party_list = []
        self.dead_party_list = []
        self.available_passes = []
        self.initiative = []

        self.bg = pygame.image.load(os.path.join("./background.png"))
        self.bg = pygame.transform.scale(self.bg, (screenWidth, screenHeight))
        
        for i in allies:
            self.spawn_ally(Character(**i))
        for i in enemies:
            self.spawn_enemy(Character(**i))
            
        for i in self.initiative:
            i.scale_stats(difficulty)
            i.randomize_spells(difficulty)

        random.shuffle(self.initiative)
        self.current_turn = 0
        self.current_character: Character = self.initiative[0]
        self.highlited_menu_item = 0
        self.selected_spell = None
        self.targeting_teammates = False
        self.selected_character = 0
        self.target = self.enemy_list[0]
        self.target_list = self.enemy_list
        self.game_state: GameState
        if self.current_character.is_enemy:
            self.game_state = GameState.WAITING_TURN
        else:
            self.game_state = GameState.DEFAULT
        
        self.target: Character
        for member in self.party_list:
            self.available_passes.append(member)

    def spawn_enemy(self, enemy: Character):
        self.initiative.append(enemy)
        self.enemy_list.append(enemy)
        enemy.is_enemy = True
        for character in self.initiative:
            character.x = 0
            character.refactor_position(self.enemy_list, self.party_list)
            
    def spawn_ally(self, ally: Character):
        self.initiative.append(ally)
        self.party_list.append(ally)
        for character in self.initiative:
            character.x = 0
            character.refactor_position(self.enemy_list, self.party_list)

    # Functions
    def render_frame(self):
        from Game import screen, screenHeight, screenWidth, panelHeight
        UI.draw_bg(self.bg)
        UI.draw_cut_in()
        pygame.draw.rect(screen, (0,0,0), (0, screenHeight, screenWidth, panelHeight))
        pygame.draw.line(screen, UI.WHITE, (0, screenHeight), (screenWidth, screenHeight), 2)
        UI.draw_characters(self.initiative, self.current_character)
        
        if self.current_character in self.party_list and self.turn_timer < 0:
            UI.draw_controls()
            if self.game_state == GameState.IN_MENU:
                UI.draw_spells(self.current_character, self.highlited_menu_item)
            else:
                UI.draw_party_health(self.party_list)
                if self.selected_spell is not None and self.selected_spell.multi_target:
                    UI.draw_chevron_all(self.enemy_list, self.targeting_teammates, self.party_list)
                else:
                    UI.draw_chevron()
        else:
            UI.draw_party_health(self.party_list)
        if self.game_over:
            UI.draw_game_ending(self.enemy_list, self.party_list, self.initiative)
            
    def next_turn(self):
        self.check_game_over()
        self.turn_timer = self.time_between_turns
        
        if self.pass_available:
            return

        self.current_turn += 1
        if (self.current_turn > len(self.initiative) - 1):
            self.current_turn = 0
            
        self.available_passes.clear()
        for member in self.party_list:
            if not member.downed:
                self.available_passes.append(member)
        self.current_character = self.initiative[self.current_turn]
        self.current_character.start_turn()
    
    def skip_turn(self):

        self.current_turn += 1
        if (self.current_turn > len(self.initiative) - 1):
                self.current_turn = 0

        self.current_character.start_turn()
        
    def manage_turn(self):
        if self.game_over:
            return

        self.turn_timer -= 1
        if (self.turn_timer > 0):
            return

        if self.current_character.is_ai:
            self.current_character.ai_logic()
        
    def input_manager(self, event):
        if self.game_state == GameState.IN_MENU:
            self.input_menu(event)
            return
                
        self.input_cursor(event)
        if self.game_state == GameState.PASSING_TURN:
            if event.key == pygame.K_b:
                self.target_list = self.enemy_list
                self.game_state = GameState.DEFAULT
            if event.key == pygame.K_z:
                self.target_list = self.enemy_list
                self.current_character = self.target
                self.game_state = GameState.DEFAULT
                self.pass_available = False
                self.current_character.defending = False
                self.current_character.pass_timer = 20
            return
                
        if event.key == pygame.K_z:
            if self.selected_spell == None:
                self.current_character.attack(self.target)
            else:
                self.current_character.use_spell(self.selected_spell, self.target)
                self.selected_spell = None
                self.targeting_teammates = False
                    
        if event.key == pygame.K_x:
            self.game_state = GameState.IN_MENU
            self.menu_list = self.current_character.spells
            self.highlited_menu_item = clamp_number_loop(self.highlited_menu_item, 0, len(self.current_character.spells) - 1)
                    
        if event.key == pygame.K_v:
            self.current_character.defend()
                    
        if self.pass_available and event.key == pygame.K_b:
            if self.available_passes:
                if self.current_character in self.available_passes:
                    self.available_passes.remove(self.current_character)
                self.target_list = self.available_passes
                self.game_state = GameState.PASSING_TURN
                        
    def input_menu(self, event: Event):
        if event.key == pygame.K_LEFT:
            self.highlited_menu_item -= 1
        if event.key == pygame.K_RIGHT:
            self.highlited_menu_item += 1
        self.highlited_menu_item = clamp_number_loop(self.highlited_menu_item, 0, len(self.menu_list) - 1)
        
        if event.key == pygame.K_UP:
            self.highlited_menu_item -= 4
        if event.key == pygame.K_DOWN:
            self.highlited_menu_item += 4
        self.highlited_menu_item = clamp_number(self.highlited_menu_item, 0, len(self.menu_list) - 1)
                    
        #Cancel
        if event.key == pygame.K_x:
            self.game_state = GameState.DEFAULT
            self.selected_spell = None
            self.targeting_teammates = False;
            self.target_list = self.enemy_list

        if event.key == pygame.K_z:
            selected_menu_item = self.menu_list[self.highlited_menu_item]
            if isinstance(selected_menu_item, HealingSpell) and selected_menu_item.revives:
                if not self.dead_party_list:
                    return
            elif isinstance(selected_menu_item, DamageSpell) and selected_menu_item.damage_type == DamageType.PHYSICAL:
                if self.current_character.hp <= selected_menu_item.cost: return
            else:
                if self.current_character.mana < selected_menu_item.cost: return
                    
            self.selected_spell = self.menu_list[self.highlited_menu_item]
            
            if type(self.selected_spell) == DamageSpell:
                self.target_list = self.enemy_list
                self.targeting_teammates = False
            elif type(self.selected_spell) == HealingSpell:
                if self.selected_spell.revives:
                    self.target_list = self.dead_party_list
                else:
                    self.target_list = self.party_list
                self.targeting_teammates = True
            self.game_state = GameState.DEFAULT

           
    def input_cursor(self, event: Event):
        if event.key == pygame.K_LEFT:
            self.selected_character -= 1
        if event.key == pygame.K_RIGHT:
            self.selected_character += 1

    def check_game_over(self):
        if not self.enemy_list:
            self.game_over = True
            return
        for member in self.party_list:
            if member.alive:
                return
        self.game_over = True
    
    def update(self):
        from Game import clock
        self.manage_turn()
    
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    import Game
                    from Menu import Menu
                    Game.menu = Menu()
                    Game.battle = None
                    return
                    
            if self.turn_timer > 0:
                return
            if self.current_character.is_ai:
                return
            if self.game_over:
                return
            
            if event.type == pygame.KEYDOWN:
                self.input_manager(event)
                
        self.selected_character = clamp_number_loop(self.selected_character, 0, len(self.target_list) - 1)
        if self.target_list:
            self.target = self.target_list[self.selected_character]
    
        self.render_frame()
        
from Game import *
