import random
import pygame
from blocks import Blocks
from setting import Setting
import block_render
class Movement():


    def __init__(self, blocks):
        self.blocks = blocks
        self.WHITE = Setting.WHITE
        self.lines = [] # 存放遊戲狀態[[0,...,0],...,[1,...,1]]
        self.imgs = [] # 存放要畫的所有方塊和座標 [image, [x, y]]
        self.draw_init()
        self.screen = Setting.screen 
        self.speed = 0.5
        # 建立遊戲狀態二維陣列
        for i in range((Setting.HEIGHT-100)//30):
            self.lines.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        for i in range(3):
            self.lines.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.gameover = False
        
    def draw_init(self):
        #隨機選擇初始圖形
        self.choose = random.choice(self.blocks.all_blocks[0:7])
        #一種圖形有不同方向 隨機選一個
        self.n = random.choice(self.choose)
        self.color = self.blocks.all_colors[self.blocks.all_blocks.index(self.choose)]
        self.Hard_Drop = False
        #方塊座標增加數值
        self.SPEEDx = 0
        self.SPEEDy = 0
        self.speed_n = 0
        #定位原點
        self.O = [-2, 4]
        
    def draw(self, ScreenState):
        if (self.speed*self.speed_n) % 30 == 0:
            self.SPEEDy = (self.speed)*self.speed_n
            self.O[0] += 1
        self.region_judge()
        for j in range(len(self.n)):
            self.X, self.Y = self.blocks.all_InitPos[self.n[j]]
            self.X += self.SPEEDx
            self.Y += self.SPEEDy
            self.Check_touch()
            if self.O[0] >= 0: O = self.O[0]
            else: O = 0
            for i in range(O, len(self.judge_list)):
                if self.judge_list[i] == False:
                    self.stop_line = i-1
                    break
                if self.judge_list.count(True) == 19:
                    self.stop_line = 18
            # 觸碰到停止線(最上方的方塊) 或 按下空白鍵
            if (self.Y-50)//30 >= self.stop_line+self.blocks.mn_dic[self.n[j]][0] or self.Hard_Drop == True:
                temp = self.HardDrop()
                if temp == 5:
                    # 繪製最後一個圖形 (略過超出邊界的方塊)
                    for k in range(len(self.n)):
                        self.X, self.Y = self.blocks.all_InitPos[self.n[k]]
                        self.X += self.SPEEDx
                        self.Y = (self.stop_line+self.blocks.mn_dic[self.n[k]][0])*30+50
                        if self.Y < 50:
                            continue
                        self.imgs.append([self.image, [self.X, self.Y]])
                        self.lines[(self.Y-50)//30][(self.X-self.blocks.CellX)//30] = 1
                        block_render.draw_fill_block(self.screen, self.X, self.Y, self.color)
                    return 5
            else:
                # 繪製圖形及落下的提示外框
                if self.Y >= 50:
                    block_render.draw_fill_block(self.screen, self.X, self.Y, self.color)

                if self.stop_line >= 0:
                    y_outline = (self.stop_line + self.blocks.mn_dic[self.n[j]][0]) * 30 + 50
                    block_render.draw_outline_block(self.screen, self.X, y_outline, self.WHITE)

        self.speed_n += 1
        return ScreenState

    # 判斷是否超出邊界
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

    # 判斷是否碰到其他方塊
    def Check_touch(self):
        self.judge_list = []
        for i in range(0, 19):
            judge_objects = 0
            for h in self.n:
                if self.lines[i+self.blocks.mn_dic[h][0]][self.O[1]+self.blocks.mn_dic[h][1]] == 0:
                    judge_objects += 1
            if judge_objects == 4:
                self.judge_list.append(True)
            else: self.judge_list.append(False)

    # 直接落下 (空白鍵)
    def HardDrop(self):
        for j in range(len(self.n)):
            self.X, self.Y = self.blocks.all_InitPos[self.n[j]]
            self.X += self.SPEEDx
            self.Y = (self.stop_line+self.blocks.mn_dic[self.n[j]][0])*30+50
            self.image = block_render.create_filled_surface(self.color)
    
            self.rect = self.image.get_rect()
            if self.Y >= 50:
                self.rect.x = self.X
                self.rect.y = self.Y
                self.imgs.append([self.image, [self.X, self.Y]])
                self.lines[(self.Y-50)//30][(self.X-self.blocks.CellX)//30] = 1
                # self.WIDTH-self.BAR_WIDTH-player1_X
                if j == 3:
                    self.draw_init()
                if self.Y == 50:
                    # self.gameover = True
                    return 5
            if self.Y < 50: 
                # self.gameover = True
                return 5


    #旋轉系統
    def rotate(self, ScreenState):
        d = self.choose.index(self.n)+1
        if d-len(self.choose) >= 0:
            d = d-len(self.choose)
        self.n = self.choose[d]
        self.draw(ScreenState)
