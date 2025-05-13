from operator import ge
import pygame
import random
import os


FPS = 125
WIDTH = 900
HEIGHT = 700
BAR_WIDTH = 300
BAR_HEIGHT = 600

BLACK = (0, 0, 0)
LIGHT_GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

#color name = (R, G, B)
ORANGE = (255, 165, 0)
PURPLE = (153, 50, 204)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (0, 245, 255)
DEEP_BLUE = (72, 61, 139)


#遊戲初始化
pygame.init()
pygame.mixer.init()
#創建視窗
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#更改檔名
pygame.display.set_caption("TETRIS")
#創建物件(管理操控時間)
clock = pygame.time.Clock()


#方塊建立(訂定座標)
T = [[1, 4, 5, 6],
     [0, 4, 5, 8],
     [0, 1, 2, 5],
     [1, 4, 5, 9]]
S = [[1, 2, 4, 5],
     [0, 4, 5, 9]]
Z = [[1, 4, 5, 8],
      [0, 1, 5, 6]]
I = [[0, 4, 8, 12],
     [4, 5, 6, 7]]
J = [[0, 4, 5, 6],
     [0, 1, 4, 8],
     [0, 1, 2, 6],
     [1, 5, 8, 9]]
L = [[2, 4, 5, 6],
     [0, 4, 8, 9],
     [0, 1, 2, 4],
     [0, 1, 5, 9]]
O = [[0, 1, 4, 5]]

all_objects = [T, Z, J, I, L, O, S]
all_colors = [PURPLE, RED, DEEP_BLUE, LIGHT_BLUE, ORANGE, YELLOW, GREEN]

init = True

class Position():
    def __init__(self):
        #各編號方塊出現的初始座標[x, y]
        self.all_spaces = {0:(220, -10), 1:(250, -10), 2:(280, -10), 3:(310, -10),
                          4:(220, 20), 5:(250, 20), 6:(280, 20), 7:(310, 20),
                          8:(220, 50), 9:(250, 50), 10:(280, 50), 11:(310, 50),
                          12:(220, 80), 13:(250, 80), 14:(280, 80), 15:(310, 80)}
        #各編號方塊在4*4格子中的[列, 行]
        self.mn_dic = {0:[0, 0], 1:[0, 1], 2:[0, 2], 3:[0, 3],
                       4:[1, 0], 5:[1, 1], 6:[1, 2], 7:[1, 3],
                       8:[2, 0], 9:[2, 1], 10:[2, 2], 11:[2, 3],
                       12:[3, 0], 13:[3, 1], 14:[3, 2], 15:[3, 3]}

class Move():
    def init(self):
        self.speed = 0.5
        self.draw_init()
        self.lines = []      
        for i in range((HEIGHT-100)//30):
            self.lines.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        for i in range(3):
            self.lines.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.imgs = []
        self.gameover = False

    def draw_init(self):
        #隨機選擇初始圖形
        self.choose = random.choice(all_objects[0:7])
        self.n = random.choice(self.choose)
        self.color = all_colors[all_objects.index(self.choose)]
        self.Go_Down = False
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
            self.X, self.Y = position.all_spaces[self.n[j]]
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
            if (self.Y-50)//30 >= self.stop_line+position.mn_dic[self.n[j]][0] or self.Go_Down == True:
                self.go_down()
            else:
                if self.Y >= 50:
                    fill_rect = pygame.Rect(self.X, self.Y, 30, 30)
                    pygame.draw.rect(screen, self.color, fill_rect)
                if self.stop_line >= 0:
                    outline_rect = pygame.Rect(self.X, (self.stop_line+position.mn_dic[self.n[j]][0])*30+50, 30, 30)
                    pygame.draw.rect(screen, WHITE, outline_rect, 3)
        self.speed_n += 1

    def region_judge(self):
        self.judge_R = []
        for i in self.n:
            self.judge_R.append(self.O[1]+position.mn_dic[i][1])
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
                if self.lines[i+position.mn_dic[h][0]][self.O[1]+position.mn_dic[h][1]] == 0:
                    judge_objects += 1
            if judge_objects == 4:
                self.judge_list.append(True)
            else: self.judge_list.append(False)

    
    def go_down(self):
        for j in range(len(self.n)):
            self.X, self.Y = position.all_spaces[self.n[j]]
            self.X += self.SPEEDx
            self.Y = (self.stop_line+position.mn_dic[self.n[j]][0])*30+50
            self.image = pygame.Surface((30, 30))
            self.image.fill(self.color)
            self.rect = self.image.get_rect()
            if self.Y >= 50:
                self.rect.x = self.X
                self.rect.y = self.Y
                self.imgs.append([self.image, [self.X, self.Y]])
                self.lines[(self.Y-50)//30][(self.X-100)//30] = 1
                if j == 3:
                    self.draw_init()
                if self.Y == 50:
                    self.gameover = True
            if self.Y < 50: 
                self.gameover = True

class Rotate():
    #旋轉系統
    def rotate(self):
        d = move.choose.index(move.n)+1
        if d-len(move.choose) >= 0:
            d = d-len(move.choose)
        move.n = move.choose[d]
        move.draw()

class Break():
    def init(self):
        self.score = 0
        self.score_old = 0
        self.level = 1

    def break_judge(self):
        for i in move.lines:
            judge_filled = 0
            for j in i:
                if j == 1 and move.lines.index(i)<=19:
                    judge_filled += 1
                else:break
            if judge_filled == 10:
                self.break_lines(move.lines.index(i))
                move.lines.remove(i)
                move.lines.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def break_lines(self, line):
        self.imgs_re = []
        self.score += int(move.speed*10)
        get_score_sound.play()
        for h in range(len(move.imgs)):
            if move.imgs[h][1][1] == line*30+50:
                self.imgs_re.append(move.imgs[h])
            elif move.imgs[h][1][1] < line*30+50:
                move.imgs[h][1][1] += 30
        for i in self.imgs_re:
            move.imgs.remove(i)

def draw_text(text, size, x, y):
    font_name = os.path.join("font.ttf")
    font = pygame.font.Font(font_name, size)
    #繪製文字(文字, 平滑值, 文字顏色, 背景顏色)
    TEXT = font.render(text, True, WHITE)
    TEXT_rect = TEXT.get_rect()
    TEXT_rect.centerx = x
    TEXT_rect.centery = y
    screen.blit(TEXT, TEXT_rect)

position = Position()
move = Move()
move.init()
rotate = Rotate()
break_line = Break()
break_line.init()

running = True

img = pygame.image.load(os.path.join("T_imgs", "level_1.jpg")).convert()
gameover_img = pygame.transform.scale(img, (200, 200))
icon = pygame.image.load(os.path.join("icon.png")).convert()
icon.set_colorkey(BLACK)
pygame.display.set_icon(icon)
pygame.mixer.music.load(os.path.join("T_sounds", "happytime.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)

get_score_sound = pygame.mixer.Sound(os.path.join("T_sounds", "score.mp3"))


while running:

    #1秒鐘內最多執行幾次
    clock.tick(FPS)

    while init == True:
        draw_text("TETRIS", 64, WIDTH//2, HEIGHT//2-100)
        draw_text("左右鍵移動 空白鍵直接落下 上鍵旋轉方塊", 32, WIDTH//2, HEIGHT//2)
        draw_text("按下任意鍵開始遊戲", 32, WIDTH//2, HEIGHT//2+100)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                init = False
                break
            if event.type == pygame.KEYUP:
                init = False
                break
            
    while move.gameover == True:
        screen.blit(gameover_img, (550, 200))
        draw_text("GAME OVER", 72, 650, 460)
        draw_text("按下任意鍵繼續遊戲", 32, 650, 550)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                move.gameover = False
            if event.type == pygame.KEYDOWN:
                move.init()
                break_line.init()

    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and move.gameover == False:
            #移動系統
            if event.key == pygame.K_SPACE:
                move.Go_Down = True
            if event.key == pygame.K_RIGHT:
                move.move("R") 
            if event.key == pygame.K_LEFT:
                move.move("L") 
            #旋轉系統
            if event.key == pygame.K_UP:
                rotate.rotate()
    
    #畫面顯示
    screen.fill(BLACK)
    
    #移動系統
    move.draw()
    for i, j in move.imgs:
        screen.blit(i, j)
    #消行系統
    break_line.break_judge()
    if break_line.score - break_line.score_old >= 80:
        break_line.score_old = break_line.score
        move.speed += 0.25
        break_line.level += 1
        
    draw_text(f"Score {break_line.score}", 32, 650, 100)
    draw_text(f"Level {break_line.level}", 32, 650, 150)

    #遊戲畫面顯示
    outline_rect = pygame.Rect(100, 50, BAR_WIDTH, BAR_HEIGHT)
    pygame.draw.rect(screen, LIGHT_GRAY, outline_rect, 2)
    for i in range(9):
        pygame.draw.line(screen, LIGHT_GRAY, (130+i*30, 50), (130+i*30, 648), 2)
    for i in range(19):
        pygame.draw.line(screen, LIGHT_GRAY, (100, 80+i*30), (398, 80+i*30), 2)
    
    pygame.display.update()
    
pygame.quit()