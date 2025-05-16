from operator import ge
import pygame
import os
from blocks import Blocks
from movement import Movement
from remove import Remove
from screenRendering import ScreenRender
from database import DataBase
from screenRendering import ScreenRender
from setting import Setting

class Player():
    BLACK = (0, 0, 0)
    LIGHT_GRAY = (128, 128, 128)
    WHITE = (255, 255, 255)
 
    def __init__(self, ScreenState, player, mode):
        self.blocks = Blocks(player, mode)
        self.movement = Movement(self.blocks)
        self.remove = Remove(self.movement)
        self.mode = mode
        self.player = player
        self.screenRender = ScreenRender(ScreenState)
        self.screen = Setting.screen
        self.ScreenState = ScreenState
        self.WIDTH = Setting.WIDTH
        self.BAR_WIDTH = Setting.BAR_WIDTH
        if mode == 1:
            self.rotate = pygame.K_UP
            self.right = pygame.K_RIGHT
            self.left = pygame.K_LEFT
            self.hardDrop = pygame.K_SPACE
        if mode == 2:
            if player == 1:
                self.rotate = pygame.K_w
                self.right = pygame.K_d
                self.left = pygame.K_a
                self.hardDrop = pygame.K_TAB
            else:
                self.rotate = pygame.K_UP
                self.right = pygame.K_RIGHT
                self.left = pygame.K_LEFT
                self.hardDrop = pygame.K_SPACE
        
    def Event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and self.movement.gameover == False:
                
                #移動系統
                if event.key == self.hardDrop:
                    self.movement.Hard_Drop = True
                if event.key == self.right:
                    self.movement.move("R") 
                if event.key == self.left:
                    self.movement.move("L")
                #旋轉系統
                if event.key == self.rotate:
                    self.movement.rotate(self.ScreenState)
            # elif event.type == pygame.TEXTINPUT:
            #     if event.text == ' ':
            #         self.movement.Hard_Drop = True
                    
    def Playing(self):
        #畫面顯示
        
        
        #移動系統
        self.ScreenState = self.movement.draw(self.ScreenState)
        for i, j in self.movement.imgs:
            self.screen.blit(i, j)
        #消行系統
        self.remove.break_judge()
        if self.remove.score - self.remove.score_old >= 80:
            self.remove.score_old = self.remove.score
            self.movement.speed += 0.25
            self.remove.level += 1   
        
        if self.mode == 1:  
            player_Y = 50
            player1_X = 600
            self.screenRender.GameCell(player1_X,player_Y,30,2,20,10)
        else:
            player_Y = 50
            player1_X = 100
            player2_X = self.WIDTH-self.BAR_WIDTH-player1_X
            self.screenRender.GameCell(player1_X,player_Y,30,2,20,10)
            self.screenRender.GameCell(player2_X,player_Y,30,2,20,10)
        if self.mode == 2 and self.player == 2:
            x = 1000
        else:
            x = 500
            
        self.screenRender.draw_text(f"Score {self.remove.score}", 32, x, 100, self.WHITE)
        self.screenRender.draw_text(f"Level {self.remove.level}", 32, x, 150, self.WHITE)
        return self.ScreenState