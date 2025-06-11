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
        self.player1_name = ""
        self.player2_name = ""
        self.input_active = False
        self.current_player = 1  # 1 for player 1, 2 for player 2
        self.input_rect = pygame.Rect(self.WIDTH//2 - 150, 300, 300, 50)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_speed = 500  # 光標閃爍速度（毫秒）
        self.composition = ""  # 用於存儲正在輸入的中文字符
        # 使用系統內建的中文字體
        self.font = pygame.font.SysFont("microsoftjhenghei", 32)
    
    def Initial(self):
        # 載入並縮放背景圖
        self.bg_img = pygame.image.load("assests/imgs/background.png")
        self.bg_img = pygame.transform.scale(self.bg_img, self.screen.get_size())
        self.screen.blit(self.bg_img, (0, 0))
        pygame.display.update()

        single_rect = pygame.Rect(820, 410, 265, 50) # 650, 410, 250, 50
        two_player_rect = pygame.Rect(820, 480, 265, 50)
        leaderboard_rect = pygame.Rect(820, 550, 265, 50)
        while True:
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if single_rect.collidepoint(mouse_pos):
                        return 1  # Single mode
                    elif two_player_rect.collidepoint(mouse_pos):
                        return 2  # Two Player mode
                    elif leaderboard_rect.collidepoint(mouse_pos):
                        return 7  # Leaderboard
                if single_rect.collidepoint(mouse_pos) or two_player_rect.collidepoint(mouse_pos) or leaderboard_rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    
        # self.screen.fill(self.WHITE)
        # self.ScreenState = self.Button(("Single",820, 410, 265, 50, 1), ("Two Player",820, 480, 265, 50, 2), ("Leaderboard", 820, 550, 265, 50, 7))
        # return self.ScreenState
        

    def SingleMode_Start(self):
        #遊戲畫面顯示
        self.screen.fill(self.BLACK)
        player_Y = 50
        player1_X = 600
        self.GameCell(player1_X,player_Y,30,2,20,10, self.player1_name)  # 添加玩家名字
        pygame.display.update()

        self.ScreenState = self.Button(("Start",300, 150, 100, 50, 3), ("Go Back", 1400, 600, 100, 50, 0))
        return self.ScreenState
                    
    def TwoPlayerMode_Start(self):
        #遊戲畫面顯示
        self.screen.fill(self.BLACK)
        player_Y = 50
        player1_X = 100
        player2_X = self.WIDTH-self.BAR_WIDTH-player1_X
        self.GameCell(player1_X,player_Y,30,2,20,10)
        self.GameCell(player2_X,player_Y,30,2,20,10)
        pygame.display.update()

        self.ScreenState = self.Button(("Start",700, 150, 100, 50, 4), ("Go Back", 1400, 600, 100, 50, 0))
        return self.ScreenState
     
    def SingleModeGameOver(self, x, y):
        # 先用黑色長方形遮住2.png
        image2 = pygame.image.load("assests/imgs/3.png").convert_alpha()
        x2, y2 = 900, 90  # 根據實際顯示位置調整
        pygame.draw.rect(self.screen, (0, 0, 0), (x2, y2, image2.get_width(), image2.get_height()))
        # 再顯示level_1.jpg
        img = pygame.image.load(os.path.join("Assests/imgs", "level_1.jpg")).convert()
        gameover_img = pygame.transform.scale(img, (200, 200))
        self.screen.blit(gameover_img, (x, y))
        self.draw_text("GAME OVER", 72, x+100, y+260, self.WHITE)
        self.ScreenState = self.Button(("Go Back", 1400, 600, 100, 50, 0))
        return self.ScreenState
        # pygame.display.update() 
    
    def TwoPlayerModeGameOver(self, player):
        # player 輸的那個
        #img = pygame.image.load(os.path.join("Assests/imgs", "level_1.jpg")).convert()
        #gameover_img = pygame.transform.scale(img, (200, 200))            
        if player == 1:
            x = 750

            text_P1 = "YOU LOSE"
            text_P2 = "YOU WIN"
            image2 = pygame.image.load("assests/imgs/3.png").convert_alpha()
            x2, y2 = 400, 200  # 根據實際顯示位置調整
            pygame.draw.rect(self.screen, (0, 0, 0), (x2, y2, 600, 250))
            text_2= self.player2_name + " WIN"
            text = self.player1_name + " LOSE"
            self.draw_text(text_2, 72, x, 250, self.WHITE)
            self.draw_text(text, 72, x, 400, self.WHITE)
            #self.screen.blit(gameover_img, (650, 200))
        elif player == 2:
            x = 750

            text_P1 = "YOU WIN"
            text_P2 = "YOU LOSE"
            image2 = pygame.image.load("assests/imgs/3.png").convert_alpha()
            x2, y2 = 400, 200  # 根據實際顯示位置調整
            pygame.draw.rect(self.screen, (0, 0, 0), (x2, y2, 600, 250))
            text_2= self.player1_name + " WIN"
            text = self.player2_name + " LOSE"
            self.draw_text(text_2, 72, x, 250, self.WHITE)
            self.draw_text(text, 72, x, 400, self.WHITE)
            #self.screen.blit(gameover_img, (650, 200))

        #if player == 1 or player == 2:
            #self.draw_text(text_P1, 72, 250, 350, self.WHITE)
            #self.draw_text(text_P2, 72, 1250, 350, self.WHITE)
        else:
            x = 750
            text = "DRAW"
            # 先用黑色長方形遮住2.png
            image2 = pygame.image.load("assests/imgs/3.png").convert_alpha()
            x2, y2 = 400, 200  # 根據實際顯示位置調整
            pygame.draw.rect(self.screen, (0, 0, 0), (x2, y2, 600, 250))
            self.draw_text(text, 72, x, 350, self.WHITE)
            
        #self.draw_text(text, 72, x, 350, self.WHITE)
        #self.draw_text("DRAW", 72, 750, 350, self.WHITE)
        self.ScreenState = self.Button(("Go Back", 1400, 600, 100, 50, 0))
        return self.ScreenState
    
                 
    def LeaderBoard(self, data):
        # 載入並顯示 top.png 作為背景
        top_img = pygame.image.load("assests/imgs/top.png").convert_alpha()
        # 將圖片縮放到整個畫面大小
        top_img = pygame.transform.scale(top_img, (Setting.WIDTH, Setting.HEIGHT))
        # 將圖片作為背景
        self.screen.blit(top_img, (0, 0))
        
        Cnt = 0
        for item in data[:5]:
            name = item["Name"]
            score = item["Score"]
            # 名字往右移動1公分（約40像素），分數位置不變
            name_x = 700 + 40  # 原本700，往右1公分
            score_x = 1100     # 分數位置保持不變
            y = 268 + Cnt
            self.draw_text(name, 60, name_x, y, self.BLACK)   # 字體縮小一點
            self.draw_text(str(score), 60, score_x, y, self.BLACK)  # 字體縮小一點
            Cnt += 80
        pygame.display.update()
        self.ScreenState = self.Button(("Go Back", 1400, 600, 100, 50, 0))    
        return self.ScreenState
            
    
    
    
    def GameCell(self, x, y, Cell_Edge, line_Width, Row_Cnt, Col_Cnt, player_name=None):
        rect = pygame.Rect(x, y, self.BAR_WIDTH, self.BAR_HEIGHT)
        pygame.draw.rect(self.screen, self.LIGHT_GRAY, rect, line_Width)
        for i in range(Col_Cnt-1):
            pygame.draw.line(self.screen, self.LIGHT_GRAY, (x+(i+1)*Cell_Edge, y), (x+(i+1)*Cell_Edge, Cell_Edge*Row_Cnt-line_Width+y), line_Width)
        for i in range(Row_Cnt-1):
            pygame.draw.line(self.screen, self.LIGHT_GRAY, (x, y+Cell_Edge+i*Cell_Edge), (Cell_Edge*Col_Cnt-line_Width+x, y+Cell_Edge+i*Cell_Edge), line_Width)
        
        # Display player name if provided
        if player_name:
            self.draw_text(player_name, 32, x + self.BAR_WIDTH//2, y - 30, self.WHITE)
            
    
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
            # self.bg_img = pygame.image.load("assests/imgs/background.png")
            # self.bg_img = pygame.transform.scale(self.bg_img, self.screen.get_size())
            # self.screen.blit(self.bg_img, (0, 0))
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

    def NameInput(self, is_two_player=False):
        # 初始化必要的屬性
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.player1_name = ""
            self.player2_name = ""
            self.input_active = True  # 預設為激活狀態
            self.current_player = 1
            self.current_name = ""  # 用於存儲當前輸入的文字
            self.color_inactive = pygame.Color('lightskyblue3')
            self.color_active = pygame.Color('dodgerblue2')
            self.cursor_visible = True
            self.cursor_timer = pygame.time.get_ticks()  # 初始化計時器
            self.composition = ""  # 用於存儲正在輸入的中文字符
            self.title_font = pygame.font.SysFont("microsoftjhenghei", 48)
            self.input_font = pygame.font.SysFont("microsoftjhenghei", 32)

        # 清除畫面
        self.screen.fill(Setting.BLACK)
        
        # 繪製標題
        if is_two_player:
            title = f"Player {self.current_player} Name"
        else:
            title = "Player 1 Name"
        title_surface = self.title_font.render(title, True, Setting.WHITE)
        title_rect = title_surface.get_rect(center=(Setting.WIDTH//2, 100))
        self.screen.blit(title_surface, title_rect)
        
        # 繪製輸入框
        input_rect = pygame.Rect(Setting.WIDTH//2 - 200, 200, 400, 50)
        pygame.draw.rect(self.screen, self.color_active if self.input_active else self.color_inactive, input_rect, 2)
        
        # 繪製當前輸入的文字
        text_surface = self.input_font.render(self.current_name + self.composition, True, Setting.WHITE)
        self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 10))
        
        # 繪製閃爍的光標
        if self.input_active and self.cursor_visible:
            cursor_x = input_rect.x + 5 + text_surface.get_width()
            pygame.draw.line(self.screen, Setting.WHITE, 
                           (cursor_x, input_rect.y + 5),
                           (cursor_x, input_rect.y + 45), 2)
        
        # 繪製提示文字
        hint_text = "Press Enter to continue"
        hint_surface = self.input_font.render(hint_text, True, Setting.WHITE)
        hint_rect = hint_surface.get_rect(center=(Setting.WIDTH//2, 300))
        self.screen.blit(hint_surface, hint_rect)
        
        # 更新畫面
        pygame.display.flip()
        
        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    self.input_active = True
                    self.cursor_visible = True
                    self.cursor_timer = pygame.time.get_ticks()
                else:
                    self.input_active = False
            elif event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_BACKSPACE:
                    if self.composition:
                        self.composition = ""
                    else:
                        self.current_name = self.current_name[:-1]
                    self.cursor_visible = True
                    self.cursor_timer = pygame.time.get_ticks()
                elif event.key == pygame.K_RETURN:
                    if self.current_name:
                        if not is_two_player:
                            self.player1_name = self.current_name
                            self.current_name = ""  # 重置輸入
                            return 1
                        else:
                            if self.current_player == 1:
                                self.player1_name = self.current_name
                                self.current_name = ""  # 重置輸入
                                self.current_player = 2  # 切換到玩家2
                                return 0  # 繼續輸入玩家2的名字
                            else:
                                self.player2_name = self.current_name
                                self.current_name = ""  # 重置輸入
                                self.current_player = 1  # 重置為玩家1
                                return 1  # 完成兩個玩家的名字輸入
            elif event.type == pygame.TEXTEDITING and self.input_active:
                self.composition = event.text
                self.cursor_visible = True
                self.cursor_timer = pygame.time.get_ticks()
            elif event.type == pygame.TEXTINPUT and self.input_active:
                if len(self.current_name + self.composition) < 10:  # 限制名字長度為10個字符
                    self.current_name += event.text
                    self.composition = ""
                    self.cursor_visible = True
                    self.cursor_timer = pygame.time.get_ticks()
        
        # 更新光標閃爍
        current_time = pygame.time.get_ticks()
        if current_time - self.cursor_timer > 500:  # 每500毫秒切換一次
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = current_time
        
        return 0