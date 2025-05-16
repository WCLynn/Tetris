import pygame
import os

class Setting():
    get_score_sound = None
    screen = None
    gameover_img = None
    FPS = 125
    WIDTH = 1500
    HEIGHT = 700
    BAR_WIDTH = 300
    BAR_HEIGHT = 600
    BLACK = (0, 0, 0)
    LIGHT_GRAY = (128, 128, 128)
    WHITE = (255, 255, 255)
    
    # def init(self, get_score_sound, gameover_img, screen):
    #     self.screen = screen
    #     self.get_score_sound = get_score_sound
    #     self.gameover_img = gameover_img