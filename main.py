from operator import ge
import pygame
import os
import sys
from screenRendering import ScreenRender
from database import DataBase
from player import Player
from setting import Setting
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

def switchLang(HKL):
    hkl = ctypes.windll.user32.LoadKeyboardLayoutW(HKL, 1)  # EN-US
    ctypes.windll.user32.ActivateKeyboardLayout(hkl, 0)
    
#遊戲初始化
pygame.init()
pygame.mixer.init()

#創建視窗
screen = pygame.display.set_mode((Setting.WIDTH, Setting.HEIGHT))
#更改檔名
pygame.display.set_caption("TETRIS")
#創建物件(管理操控時間)
clock = pygame.time.Clock()

init = True


def Quit(events):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

running = True


icon = pygame.image.load(os.path.join("Assests/imgs", "icon.png")).convert()
icon.set_colorkey(Setting.BLACK)
pygame.display.set_icon(icon)
pygame.mixer.music.load(os.path.join("Assests/sounds", "happytime.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)

Setting.screen = screen
Setting.get_score_sound = pygame.mixer.Sound(os.path.join("Assests/sounds", "score.mp3"))
img = pygame.image.load(os.path.join("Assests/imgs", "level_1.jpg")).convert()
Setting.gameover_img = pygame.transform.scale(img, (200, 200))
Setting.Button_sound = pygame.mixer.Sound(os.path.join("Assests/sounds", "Button.wav"))

ScreenState = 0
screenRender = ScreenRender(ScreenState)
database = DataBase()
state1 = 4
state2 = 4

while True:
    #1秒鐘內最多執行幾次
    clock.tick(Setting.FPS)
    events = pygame.event.get()
    Quit(events)
    
    # 只要ScreenState != 7 (不是Leaderboard頁面) 前五名資料就為空 -> 若TOP5_Data為空才從資料庫取資料 持續停留在7才不會重複取資料
    if ScreenState != 7:
        database.TOP5_Data = []

    if ScreenState == 0:  # 初始畫面 Choose Mode
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        player1 = Player(ScreenState, 1, 1)
        player12 = Player(ScreenState, 1, 2)
        player22 = Player(ScreenState, 2, 2)
        ScreenState = screenRender.Initial()

    if ScreenState == 1:  # Single mode start
        name_state = 0
        while name_state != 1:
            name_state = screenRender.NameInput(is_two_player=False)
        ScreenState = screenRender.SingleMode_Start()
    
    elif ScreenState == 2:  # Two Player mode start
        name_state = 0
        while name_state != 1:
            name_state = screenRender.NameInput(is_two_player=True)
        ScreenState = screenRender.TwoPlayerMode_Start()
    
    elif ScreenState == 3:  # Single mode playing
        switchLang("00000409")
        # 畫面顯示
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        screen.fill(Setting.BLACK)
        player1.ScreenState = ScreenState
        player1.Event(events)
        image = pygame.image.load("assests/imgs/1.png").convert_alpha()
        screen.blit(image, (100, 400))
        # 在圖片上方顯示玩家名字
        screenRender.draw_text(screenRender.player1_name, 32, 100 + image.get_width()//2, 400 - 30, Setting.WHITE)
        # 顯示圖片3於右上角
        image3 = pygame.image.load("assests/imgs/3.png").convert_alpha()
        # 設定新寬度
        new_width = 450
        # 等比例縮放
        scale_factor = new_width / image3.get_width()
        new_height = int(image3.get_height() * scale_factor)
        image3 = pygame.transform.scale(image3, (new_width, new_height))
        screen.blit(image3, (Setting.WIDTH - new_width - 20, 80))
        # 遊玩區域
        ScreenState = player1.Playing()
        pygame.display.update()

    elif ScreenState == 4:  # Two Player mode playing
        switchLang("00000409")
        # 畫面顯示
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        screen.fill(Setting.BLACK)
        # 顯示圖片5於左上角
        image5 = pygame.image.load("assests/imgs/5.png").convert_alpha()
        new_width5 = 120
        scale_factor5 = new_width5 / image5.get_width()
        new_height5 = int(image5.get_height() * scale_factor5)
        image5 = pygame.transform.scale(image5, (new_width5, new_height5))
        screen.blit(image5, (450, 500))
        # 顯示圖片6於右上角
        image6 = pygame.image.load("assests/imgs/6.png").convert_alpha()
        new_width6 = 120
        scale_factor6 = new_width6 / image6.get_width()
        new_height6 = int(image6.get_height() * scale_factor6)
        image6 = pygame.transform.scale(image6, (new_width6, new_height6))
        screen.blit(image6, (Setting.WIDTH - new_width6 - 450, 450))

        image9 = pygame.image.load("assests/imgs/9.png").convert_alpha()
        # 設定新寬度
        new_width = 500
        # 等比例縮放
        scale_factor = new_width / image9.get_width()
        new_height = int(image9.get_height() * scale_factor)
        image9 = pygame.transform.scale(image9, (new_width, new_height))
        screen.blit(image9, (Setting.WIDTH - new_width - 500, 200))
        screenRender.draw_text(f"Score {player12.remove.score}", 32, 500, 100, Setting.WHITE)
        screenRender.draw_text(f"Level {player12.remove.level}", 32, 500, 150, Setting.WHITE)
        screenRender.draw_text(f"Score {player22.remove.score}", 32, 1000, 100, Setting.WHITE)
        screenRender.draw_text(f"Level {player22.remove.level}", 32, 1000, 150, Setting.WHITE) 

        screenRender.GameCell(player1_X, player_Y, 30, 2, 20, 10, screenRender.player1_name)
        screenRender.GameCell(player2_X, player_Y, 30, 2, 20, 10, screenRender.player2_name)
        # 先讓兩個都收到事件
        if state1 != 5:
            player12.ScreenState = ScreenState
        if state2 != 5:
            player22.ScreenState = ScreenState
        if state1 != 5:
            player12.Event(events)
        if state2 != 5:
            player22.Event(events)
            
        # (遊玩區域)再讓兩個都執行遊戲邏輯（比如移動、判定等）
        if state1 != 5:
            state1 = player12.Playing(1, player22.ScreenState)
        if state2 != 5:
            state2 = player22.Playing(2, player12.ScreenState)

        player_Y = 50
        player1_X = 100
        player2_X = Setting.WIDTH-Setting.BAR_WIDTH-player1_X
        
        # 當一位玩家結束時顯示game over圖片（只在另一方還沒結束時顯示）
        if state1 == 5 and state2 != 5:
            for i, j in player12.movement.imgs:
                player12.screen.blit(i, j)  
            screenRender.GameCell(player1_X, player_Y, 30, 2, 20, 10, screenRender.player1_name)
            screenRender.GameCell(player2_X, player_Y, 30, 2, 20, 10, screenRender.player2_name) 
            img = pygame.image.load(os.path.join("Assests/imgs", "level_1.jpg")).convert()
            #gameover_img = pygame.transform.scale(img, (200, 200))
            screen.blit(Setting.gameover_img, (250, 500))
            screenRender.draw_text("GAME OVER", 72, 250, 500, Setting.WHITE)

        if state2 == 5 and state1 != 5:
            for i, j in player22.movement.imgs:
                player22.screen.blit(i, j)  
            screenRender.GameCell(player1_X, player_Y, 30, 2, 20, 10, screenRender.player1_name)
            screenRender.GameCell(player2_X, player_Y, 30, 2, 20, 10, screenRender.player2_name)
            img = pygame.image.load(os.path.join("Assests/imgs", "level_1.jpg")).convert()
            # gameover_img = pygame.transform.scale(img, (200, 200))
            screen.blit(Setting.gameover_img, (1250, 500))
            screenRender.draw_text("GAME OVER", 72, 1250, 500, Setting.WHITE)
            
        # 當兩位玩家都結束遊戲時才進入結算畫面
        if state1 == 5 and state2 == 5:
            state1 = 4
            state2 = 4
            ScreenState = 6
            for i, j in player12.movement.imgs:
                player12.screen.blit(i, j)    
            for i, j in player22.movement.imgs:
                player22.screen.blit(i, j)  
            screenRender.GameCell(player1_X, player_Y, 30, 2, 20, 10, screenRender.player1_name)
            screenRender.GameCell(player2_X, player_Y, 30, 2, 20, 10, screenRender.player2_name)
                
        pygame.display.update()

    elif ScreenState == 5:  # Single Mode GameOver
        switchLang("00000404")
        ScreenState = screenRender.SingleModeGameOver(1100, 200)
        pygame.display.update()
        database.Update_Score(screenRender.player1_name, player1.remove.score)
    
    elif ScreenState == 6:  # Two Player Mode GameOver
        switchLang("00000404")
        if player12.remove.score < player22.remove.score:
            ScreenState = screenRender.TwoPlayerModeGameOver(player12, player22,1)
        elif player12.remove.score > player22.remove.score:
            ScreenState = screenRender.TwoPlayerModeGameOver(player12, player22,2)
        else:
            ScreenState = screenRender.TwoPlayerModeGameOver(player12, player22,3)

        pygame.display.update()
        database.Update_Score(screenRender.player1_name, player12.remove.score)
        database.Update_Score(screenRender.player2_name, player22.remove.score)
    
    elif ScreenState == 7:  # Leaderboard
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if not database.TOP5_Data:
            database.TOP5_Data = database.Get_Top10()
        ScreenState = screenRender.LeaderBoard(database.TOP5_Data)