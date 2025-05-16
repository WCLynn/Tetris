from operator import ge
import pygame
import os
from blocks import Blocks
from movement import Movement
from remove import Remove
from screenRendering import ScreenRender
from database import DataBase
from player import Player
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
state1 = 4
state2 = 4
while running:

    #1秒鐘內最多執行幾次
    clock.tick(FPS)
    events = pygame.event.get()
    Quit(events)
    
    if ScreenState != 7:
        database.TOP10_Data = []
    
    if ScreenState == 0: # 初始畫面 Choose Mode
        player1 = Player(screen, HEIGHT, get_score_sound, ScreenState, 1, 1,  WIDTH, BAR_WIDTH, BAR_HEIGHT)
        player12 = Player(screen, HEIGHT, get_score_sound, ScreenState, 1, 2,  WIDTH, BAR_WIDTH, BAR_HEIGHT)
        player22 = Player(screen, HEIGHT, get_score_sound, ScreenState, 2, 2,  WIDTH, BAR_WIDTH, BAR_HEIGHT)
        ScreenState = screenRender.Initial()
        print("ScreenState: ", ScreenState)
        continue
        
    if ScreenState == 1: # Single mode start
        ScreenState = screenRender.SingleMode_Start()
        print("ScreenState: ", ScreenState)
        continue
        
    if ScreenState == 2: # Two Player mode start
        ScreenState = screenRender.TwoPlayerMode_Start()
        print("ScreenState: ", ScreenState)
        continue

    if ScreenState == 3: # Single mode playing
        screen.fill(BLACK)
        player1.ScreenState = ScreenState
        player1.Event(events)
        ScreenState = player1.Playing()
        pygame.display.update()
        continue

    
    if ScreenState == 4: # Two Player mode playing
        screen.fill(BLACK)
        
        # 先讓兩個都收到事件
        if state1 != 5:
            player12.ScreenState = ScreenState
        if state2 != 5:
            player22.ScreenState = ScreenState
        if state1 != 5:
            player12.Event(events)
        if state2 != 5:
            player22.Event(events)

        # 再讓兩個都執行遊戲邏輯（比如移動、判定等）
        if state1 != 5:
            state1 = player12.Playing()
        if state2 != 5:
            state2 = player22.Playing()

        # 根據情況決定最終的 ScreenState（例如某人Game Over）
        # if state1 != ScreenState:
        #     ScreenState = state1
        # elif state2 != ScreenState:
        #     ScreenState = state2
        pygame.display.update()
        if state1 == state2 == 5:
            state1 = 4
            state2 = 4
            if player12.remove.score < player22.remove.score:
                ScreenState = screenRender.TwoPlayerModeGameOver(1)
            elif player12.remove.score > player22.remove.score:
                ScreenState = screenRender.TwoPlayerModeGameOver(2)
            else:
                ScreenState = screenRender.TwoPlayerModeGameOver(3)
                pass

        pygame.display.update()
        continue
    
    if ScreenState == 5: # Single Mode GameOver
        database.Update_Score("Temp", player1.remove.score)
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