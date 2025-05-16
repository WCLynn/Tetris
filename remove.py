from movement import Movement
import pygame
import os
class Remove():
    
    
    
    def __init__(self, get_score_sound, HEIGHT, screen, movement):
        # self.movement = Movement(HEIGHT, screen)
        self.movement = movement
        self.score = 0
        self.score_old = 0
        self.level = 1
        self.get_score_sound = get_score_sound
    
    
    def init(self, get_score_sound):
        self.score = 0
        self.score_old = 0
        self.level = 1
        self.get_score_sound = get_score_sound

    def break_judge(self):
        for i in self.movement.lines:
            judge_filled = 0
            for j in i:
                if j == 1 and self.movement.lines.index(i)<=19:
                    judge_filled += 1
                else:break
            if judge_filled == 10:
                self.break_lines(self.movement.lines.index(i))
                self.movement.lines.remove(i)
                self.movement.lines.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                

    def break_lines(self, line):
        self.imgs_re = []
        self.score += int(self.movement.speed*10)
        self.get_score_sound.play()
        for h in range(len(self.movement.imgs)):
            if self.movement.imgs[h][1][1] == line*30+50:
                self.imgs_re.append(self.movement.imgs[h])
            elif self.movement.imgs[h][1][1] < line*30+50:
                self.movement.imgs[h][1][1] += 30
        for i in self.imgs_re:
            self.movement.imgs.remove(i)