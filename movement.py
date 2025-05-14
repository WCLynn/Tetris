import random
import pygame
from blocks import Blocks
class Movement():

    # 所有Movement物件共用變數
    blocks = Blocks()
    WHITE = (255, 255, 255)
    lines = []
    imgs = []
    speed = 0.5
        
    def init(self, HEIGHT, screen):
        self.draw_init()
        self.screen = screen  
        self.lines.clear()  
        self.imgs.clear()
        self.speed = 0.5
        for i in range((HEIGHT-100)//30):
            self.lines.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        for i in range(3):
            self.lines.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.gameover = False

    def draw_init(self):
        #隨機選擇初始圖形
        self.choose = random.choice(self.blocks.all_blocks[0:7])
        self.n = random.choice(self.choose)
        self.color = self.blocks.all_colors[self.blocks.all_blocks.index(self.choose)]
        self.Hard_Drop = False
        #方塊座標增加數值
        self.SPEEDx = 0
        self.SPEEDy = 0
        self.speed_n = 0
        #定位原點
        self.O = [-2, 4]
        
    def draw(self):
        if (self.speed*self.speed_n) % 30 == 0:
            self.SPEEDy = (self.speed)*self.speed_n
            self.O[0] += 1
        self.region_judge()
        for j in range(len(self.n)):
            self.X, self.Y = self.blocks.P1_all_InitPos[self.n[j]]
            self.X += self.SPEEDx
            self.Y += self.SPEEDy
            self.judge_touch()
            if self.O[0] >= 0: O = self.O[0]
            else: O = 0
            for i in range(O, len(self.judge_list)):
                if self.judge_list[i] == False:
                    self.stop_line = i-1
                    break
                if self.judge_list.count(True) == 19:
                    self.stop_line = 18
            if (self.Y-50)//30 >= self.stop_line+self.blocks.mn_dic[self.n[j]][0] or self.Hard_Drop == True:
                self.HardDrop()
            else:
                if self.Y >= 50:
                    fill_rect = pygame.Rect(self.X, self.Y, 30, 30)
                    pygame.draw.rect(self.screen, self.color, fill_rect)
                if self.stop_line >= 0:
                    outline_rect = pygame.Rect(self.X, (self.stop_line+self.blocks.mn_dic[self.n[j]][0])*30+50, 30, 30)
                    pygame.draw.rect(self.screen, self.WHITE, outline_rect, 3)
        self.speed_n += 1

    def region_judge(self):
        self.judge_R = []
        for i in self.n:
            self.judge_R.append(self.O[1]+self.blocks.mn_dic[i][1])
        if max(self.judge_R) > 9:
            self.O[1] -= max(self.judge_R)-9
            self.SPEEDx -= 30*(max(self.judge_R)-9)
        if min(self.judge_R) < 0:
            self.O[1] -= min(self.judge_R)
            self.SPEEDx -= 30*min(self.judge_R)

    def move(self, direction):
        if direction == "R":
            self.O[1] += 1
            self.SPEEDx += 30
        if direction == "L":
            self.O[1] -= 1
            self.SPEEDx -= 30

    def judge_touch(self):
        self.judge_list = []
        for i in range(0, 19):
            judge_objects = 0
            for h in self.n:
                if self.lines[i+self.blocks.mn_dic[h][0]][self.O[1]+self.blocks.mn_dic[h][1]] == 0:
                    judge_objects += 1
            if judge_objects == 4:
                self.judge_list.append(True)
            else: self.judge_list.append(False)

    
    def HardDrop(self):
        for j in range(len(self.n)):
            self.X, self.Y = self.blocks.P1_all_InitPos[self.n[j]]
            self.X += self.SPEEDx
            self.Y = (self.stop_line+self.blocks.mn_dic[self.n[j]][0])*30+50
            self.image = pygame.Surface((30, 30))
            self.image.fill(self.color)
            self.rect = self.image.get_rect()
            if self.Y >= 50:
                self.rect.x = self.X
                self.rect.y = self.Y
                self.imgs.append([self.image, [self.X, self.Y]])
                self.lines[(self.Y-50)//30][(self.X-600)//30] = 1 # self.X-100
                if j == 3:
                    self.draw_init()
                if self.Y == 50:
                    self.gameover = True
            if self.Y < 50: 
                self.gameover = True


    #旋轉系統
    def rotate(self):
        d = self.choose.index(self.n)+1
        if d-len(self.choose) >= 0:
            d = d-len(self.choose)
        self.n = self.choose[d]
        self.draw()
