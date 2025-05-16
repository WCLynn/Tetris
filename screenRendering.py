import pygame
import os
from database import DataBase
from setting import Setting
class ScreenRender():
    
    BLACK = (0, 0, 0)
    LIGHT_GRAY = (128, 128, 128)
    WHITE = (255, 255, 255)
    database = DataBase()
    
    def __init__(self, ScreenState):
        self.screen = Setting.screen
        self.ScreenState = ScreenState
        self.WIDTH = Setting.WIDTH
        self.BAR_WIDTH = Setting.BAR_WIDTH
        self.BAR_HEIGHT = Setting.BAR_HEIGHT
    
    def Initial(self):
        self.screen.fill(self.WHITE)
        self.ScreenState = self.Button(("Single",150, 120, 150, 50, 1), ("Two Player",150, 480, 150, 50, 2), ("Leaderboard", 300, 190, 180, 50, 7))
        return self.ScreenState
        

    def SingleMode_Start(self):
        #遊戲畫面顯示
        player_Y = 50
        player1_X = 600
        self.GameCell(player1_X,player_Y,30,2,20,10)
        pygame.display.update()

        self.ScreenState = self.Button(("Start",300, 150, 100, 50, 3), ("Go Back", 1400, 600, 100, 50, 0))
        return self.ScreenState
                    
    def TwoPlayerMode_Start(self):
        #遊戲畫面顯示
        player_Y = 50
        player1_X = 100
        player2_X = self.WIDTH-self.BAR_WIDTH-player1_X
        self.GameCell(player1_X,player_Y,30,2,20,10)
        self.GameCell(player2_X,player_Y,30,2,20,10)
        pygame.display.update()

        self.ScreenState = self.Button(("Start",700, 150, 100, 50, 4), ("Go Back", 1400, 600, 100, 50, 0))
        return self.ScreenState
     
    def SingleModeGameOver(self, x, y):
        img = pygame.image.load(os.path.join("Assests/imgs", "level_1.jpg")).convert()
        gameover_img = pygame.transform.scale(img, (200, 200))
        self.screen.blit(gameover_img, (x, y))
        self.draw_text("GAME OVER", 72, x+100, y+260, self.WHITE)
        self.ScreenState = self.Button(("Go Back", 1400, 600, 100, 50, 0))
        return self.ScreenState
        # pygame.display.update() 
    
    def TwoPlayerModeGameOver(self, player):
        img = pygame.image.load(os.path.join("Assests/imgs", "level_1.jpg")).convert()
        gameover_img = pygame.transform.scale(img, (200, 200))            
        if player == 1:
            x = 250
            text = "GAME OVER"
            self.screen.blit(gameover_img, (650, 200))
        elif player == 2:
            x = 1250
            text = "GAME OVER"
            self.screen.blit(gameover_img, (650, 200))
        else:
            x = 750
            text = "DRAW"
        
        self.draw_text(text, 72, x, 350, self.WHITE)
        self.ScreenState = self.Button(("Go Back", 1400, 600, 100, 50, 0))
        return self.ScreenState
    
                 
    def LeaderBoard(self, data):
        
        Cnt = 0
        for item in data:
            name = item["Name"]
            score = item["Score"]
            writeLine = f"Name: {name}  |   Score: {score}"
            self.draw_text(writeLine, 72, 1000, 50+Cnt, self.BLACK)
            Cnt += 50
        pygame.display.update()
        self.ScreenState = self.Button(("Go Back", 1400, 600, 100, 50, 0))    
        return self.ScreenState
            
    
    
    
    def GameCell(self, x, y, Cell_Edge, line_Width, Row_Cnt, Col_Cnt):
        rect = pygame.Rect(x, y, self.BAR_WIDTH, self.BAR_HEIGHT)
        pygame.draw.rect(self.screen, self.LIGHT_GRAY, rect, line_Width)
        for i in range(Col_Cnt-1):
            pygame.draw.line(self.screen, self.LIGHT_GRAY, (x+(i+1)*Cell_Edge, y), (x+(i+1)*Cell_Edge, Cell_Edge*Row_Cnt-line_Width+y), line_Width)
        for i in range(Row_Cnt-1):
            pygame.draw.line(self.screen, self.LIGHT_GRAY, (x, y+Cell_Edge+i*Cell_Edge), (Cell_Edge*Col_Cnt-line_Width+x, y+Cell_Edge+i*Cell_Edge), line_Width)
            
    
    def draw_text(self, text, size, x, y, color):
        font_name = os.path.join("Assests/fonts", "font.ttf")
        font = pygame.font.Font(font_name, size)
        #繪製文字(文字, 平滑值, 文字顏色, 背景顏色)
        TEXT = font.render(text, True, color)
        TEXT_rect = TEXT.get_rect()
        TEXT_rect.centerx = x
        TEXT_rect.centery = y
        self.screen.blit(TEXT, TEXT_rect)
        # pygame.display.update()
        



    # self.Buttons(
    # ("開始遊戲", 100, 100, 150, 50, 0),
    # ("設定",     100, 200, 150, 50, 0, (128, 0, 255), (200, 0, 255), (255, 255, 0)),
    # ("離開",     100, 300, 150, 50, 0)
    # )
    def Button(self, *buttons):
        default_color = (0, 128, 255)
        default_hover_color = (0, 200, 255)
        default_txt_color = (255, 255, 255)
        font = pygame.font.SysFont(None, 36)
        
        running = True 
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            
            hovering = False  # 這個變數幫你記錄滑鼠有沒有 hover 到任一個按鈕

            for button in buttons:
                text, x, y, width, height, ScreenState, *optional = button
                color = optional[0] if len(optional) > 0 else default_color
                hover_color = optional[1] if len(optional) > 1 else default_hover_color
                txt_color = optional[2] if len(optional) > 2 else default_txt_color
                button_rect = pygame.Rect(x, y, width, height)
                text_surface = font.render(text, True, txt_color)

                if button_rect.collidepoint(mouse_pos):
                    hovering = True  # 記得有 hover 到
                    pygame.draw.rect(self.screen, hover_color, button_rect)
                    if click[0]:
                        self.screen.fill(self.WHITE)
                        pygame.display.update()
                        return ScreenState
                else:
                    pygame.draw.rect(self.screen, color, button_rect)

                # 畫文字
                text_rect = text_surface.get_rect(center=button_rect.center)
                self.screen.blit(text_surface, text_rect)

            # 根據 hover 狀態統一更新鼠標形狀（只更新一次）
            if hovering:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()