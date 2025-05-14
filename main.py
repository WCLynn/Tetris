from operator import ge
import pygame
import os
from blocks import Blocks
from movement import Movement
from remove import Remove
from screenRendering import ScreenRender
FPS = 125
WIDTH = 1500
HEIGHT = 700
BAR_WIDTH = 300
BAR_HEIGHT = 600

#color name = (R, G, B)
BLACK = (0, 0, 0)
LIGHT_GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

#遊戲初始化
pygame.init()
pygame.mixer.init()
#創建視窗
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#更改檔名
pygame.display.set_caption("TETRIS")
#創建物件(管理操控時間)
clock = pygame.time.Clock()

init = True
font_name = os.path.join("Assests/fonts", "font.ttf")
def draw_text(text, size, x, y):
    font_name = os.path.join("Assests/fonts", "font.ttf")
    font = pygame.font.Font(font_name, size)
    #繪製文字(文字, 平滑值, 文字顏色, 背景顏色)
    TEXT = font.render(text, True, WHITE)
    TEXT_rect = TEXT.get_rect()
    TEXT_rect.centerx = x
    TEXT_rect.centery = y
    screen.blit(TEXT, TEXT_rect)

def Quit(events):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

running = True

img = pygame.image.load(os.path.join("Assests/imgs", "level_1.jpg")).convert()
gameover_img = pygame.transform.scale(img, (200, 200))
icon = pygame.image.load(os.path.join("Assests/imgs", "icon.png")).convert()
icon.set_colorkey(BLACK)
pygame.display.set_icon(icon)
pygame.mixer.music.load(os.path.join("Assests/sounds", "happytime.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)
get_score_sound = pygame.mixer.Sound(os.path.join("Assests/sounds", "score.mp3"))

#創建類別物件
blocks = Blocks()
movement = Movement()
movement.init(HEIGHT, screen)
remove = Remove()
remove.init(get_score_sound)
ScreenState = 0
screenRender = ScreenRender(screen, ScreenState, WIDTH, BAR_WIDTH, BAR_HEIGHT)


while running:

    #1秒鐘內最多執行幾次
    clock.tick(FPS)
    
    # while init == True:
    #     draw_text("TETRIS", 64, WIDTH//2, HEIGHT//2-100)
    #     draw_text("左右鍵移動 空白鍵直接落下 上鍵旋轉方塊", 32, WIDTH//2, HEIGHT//2)
    #     draw_text("按下任意鍵開始遊戲", 32, WIDTH//2, HEIGHT//2+100)
    #     pygame.display.update()
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #             init = False
    #             break
    #         if event.type == pygame.KEYUP:
    #             init = False
    #             break
    events = pygame.event.get()
    Quit(events)
    if ScreenState == 0: # 初始畫面 Choose Mode
        ScreenState = screenRender.Initial()
        
    if ScreenState == 1: # Single mode start
        ScreenState = screenRender.SingleMode_Start()
        
    if ScreenState == 2: # Double mode start
        ScreenState = screenRender.DoubleMode_Start()
        
    if ScreenState == 3: # Single mode playing
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and movement.gameover == False:
                #移動系統
                if event.key == pygame.K_SPACE:
                    movement.Hard_Drop = True
                if event.key == pygame.K_RIGHT:
                    movement.move("R") 
                if event.key == pygame.K_LEFT:
                    movement.move("L")
                #旋轉系統
                if event.key == pygame.K_UP:
                    movement.rotate()
            elif event.type == pygame.TEXTINPUT:
                if event.text == ' ':
                    movement.Hard_Drop = True
        
        #畫面顯示
        screen.fill(BLACK)
        
        #移動系統
        movement.draw()
        for i, j in movement.imgs:
            screen.blit(i, j)
        #消行系統
        remove.break_judge()
        if remove.score - remove.score_old >= 80:
            remove.score_old = remove.score
            movement.speed += 0.25
            remove.level += 1   
            
        player_Y = 50
        player1_X = 600
        screenRender.GameCell(player1_X,player_Y,30,2,20,10)
        
        pygame.display.update()
    
    
    
    
    

    # while movement.gameover == True:
    #     screen.blit(gameover_img, (550, 200))
    #     draw_text("GAME OVER", 72, 650, 460)
    #     draw_text("按下任意鍵繼續遊戲", 32, 650, 550)
    #     pygame.display.update()
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #             movement.gameover = False
    #         if event.type == pygame.KEYDOWN or event.type == pygame.TEXTINPUT:
    #             movement.init(HEIGHT, screen)
    #             remove.init(get_score_sound)

    # #取得輸入
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False
    #     if event.type == pygame.KEYDOWN and movement.gameover == False:
    #         #移動系統
            
    #         if event.key == pygame.K_LSHIFT:
    #             movement.Hard_Drop = True
    #         if event.key == pygame.K_d:
    #             movement.move("R") 
    #         if event.key == pygame.K_a:
    #             movement.move("L")
    #         #旋轉系統
    #         if event.key == pygame.K_w:
    #             movement.rotate()
    #     # elif event.type == pygame.TEXTINPUT:
    #     #     if event.text == ' ':
    #     #         movement.Hard_Drop = True
    
    # #畫面顯示
    # screen.fill(BLACK)
    
    # #移動系統
    # movement.draw()
    # for i, j in movement.imgs:
    #     screen.blit(i, j)
    # #消行系統
    # remove.break_judge()
    # if remove.score - remove.score_old >= 80:
    #     remove.score_old = remove.score
    #     movement.speed += 0.25
    #     remove.level += 1
        
    # draw_text(f"Score {remove.score}", 32, 650, 100)
    # draw_text(f"Level {remove.level}", 32, 650, 150)

    # #遊戲畫面顯示
    # player_Y = 50
    # player1_X = 100
    # player2_X = WIDTH-BAR_WIDTH-player1_X
    # Cell_Edge = 30
    # line_Width = 2
    # Row_Cnt = 20
    # Col_Cnt = 10
    # outline_rect_p1 = pygame.Rect(player1_X, player_Y, BAR_WIDTH, BAR_HEIGHT)
    # outline_rect_p2 = pygame.Rect(player2_X, player_Y, BAR_WIDTH, BAR_HEIGHT)
    
    # for rect, x in [(outline_rect_p1, player1_X), (outline_rect_p2, player2_X)]:
    #     pygame.draw.rect(screen, LIGHT_GRAY, rect, line_Width)
    #     for i in range(Col_Cnt-1):
    #         pygame.draw.line(screen, LIGHT_GRAY, (x+(i+1)*Cell_Edge, player_Y), (x+(i+1)*Cell_Edge, Cell_Edge*Row_Cnt-line_Width+player_Y), line_Width)
    #     for i in range(Row_Cnt-1):
    #         pygame.draw.line(screen, LIGHT_GRAY, (x, player_Y+Cell_Edge+i*Cell_Edge), (Cell_Edge*Col_Cnt-line_Width+x, player_Y+Cell_Edge+i*Cell_Edge), line_Width)

    # pygame.display.update()
    
pygame.quit()