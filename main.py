from operator import ge
import pygame
import os
from blocks import Blocks
from movement import Movement
from remove import Remove
from screenRendering import ScreenRender
from database import DataBase

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

ScreenState = 0
screenRender = ScreenRender(screen, ScreenState, WIDTH, BAR_WIDTH, BAR_HEIGHT)
database = DataBase()

while running:

    #1秒鐘內最多執行幾次
    clock.tick(FPS)
    events = pygame.event.get()
    Quit(events)
    
    if ScreenState != 7:
        database.TOP10_Data = []
    
    if ScreenState == 0: # 初始畫面 Choose Mode
        remove = Remove(get_score_sound, HEIGHT, screen)
        movement = remove.movement
        blocks = movement.blocks
        ScreenState = screenRender.Initial()
        continue
        
    if ScreenState == 1: # Single mode start
        ScreenState = screenRender.SingleMode_Start()
        continue
        
    if ScreenState == 2: # Two Player mode start
        ScreenState = screenRender.TwoPlayerMode_Start()
        continue

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
                    movement.rotate(ScreenState)
            elif event.type == pygame.TEXTINPUT:
                if event.text == ' ':
                    movement.Hard_Drop = True
        
        #畫面顯示
        screen.fill(BLACK)
        
        #移動系統
        ScreenState = movement.draw(ScreenState)
        print("ScreenState: ", ScreenState)
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
        
        screenRender.draw_text(f"Score {remove.score}", 32, 500, 100, WHITE)
        screenRender.draw_text(f"Level {remove.level}", 32, 500, 150, WHITE)
        pygame.display.update()
        continue

    
    if ScreenState == 4: # Two Player mode playing
        pass
        continue
    
    if ScreenState == 5: # Single Mode GameOver
        database.Update_Score("Temp", remove.score)
        ScreenState = screenRender.SingleModeGameOver(1100, 200)
        pygame.display.update()
        continue

    if ScreenState == 6: # Two Player Mode GameOver
        pass
        continue
    
    if ScreenState == 7: # Leaderboard
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if not database.TOP10_Data:
            database.TOP10_Data = database.Get_Top10()
            print(database.TOP10_Data)
        ScreenState = screenRender.LeaderBoard(database.TOP10_Data)
        continue
    
pygame.quit()