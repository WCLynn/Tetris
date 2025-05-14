import pygame
import os
class ScreenRender():
    
    BLACK = (0, 0, 0)
    LIGHT_GRAY = (128, 128, 128)
    WHITE = (255, 255, 255)
    
    def __init__(self, screen, ScreenState, WIDTH, BAR_WIDTH, BAR_HEIGHT):
        self.screen = screen
        self.ScreenState = ScreenState
        self.WIDTH = WIDTH
        self.BAR_WIDTH = BAR_WIDTH
        self.BAR_HEIGHT = BAR_HEIGHT
    
    def Initial(self):
        self.screen.fill(self.WHITE)
        self.ScreenState = self.Button(("Single",150, 120, 100, 50, 1), ("Double",150, 480, 100, 50, 2))
        if self.ScreenState == 1 or 2:
            return self.ScreenState
        

    def SingleMode_Start(self):
        #遊戲畫面顯示
        player_Y = 50
        player1_X = 600
        self.GameCell(player1_X,player_Y,30,2,20,10)
        pygame.display.update()

        self.ScreenState = self.Button(("Start",300, 150, 100, 50, 3))
        # pygame.display.update()
        if self.ScreenState == 3:
            return self.ScreenState
                    
    def DoubleMode_Start(self):
        #遊戲畫面顯示
        player_Y = 50
        player1_X = 100
        player2_X = self.WIDTH-self.BAR_WIDTH-player1_X
        self.GameCell(player1_X,player_Y,30,2,20,10)
        self.GameCell(player2_X,player_Y,30,2,20,10)
        pygame.display.update()

        self.ScreenState = self.Button(("Start",700, 150, 100, 50, 4))
        if self.ScreenState == 4:
            return self.ScreenState
        
       
            

                    
    
    def GameCell(self, x, y, Cell_Edge, line_Width, Row_Cnt, Col_Cnt):
        rect = pygame.Rect(x, y, self.BAR_WIDTH, self.BAR_HEIGHT)
        pygame.draw.rect(self.screen, self.LIGHT_GRAY, rect, line_Width)
        for i in range(Col_Cnt-1):
            pygame.draw.line(self.screen, self.LIGHT_GRAY, (x+(i+1)*Cell_Edge, y), (x+(i+1)*Cell_Edge, Cell_Edge*Row_Cnt-line_Width+y), line_Width)
        for i in range(Row_Cnt-1):
            pygame.draw.line(self.screen, self.LIGHT_GRAY, (x, y+Cell_Edge+i*Cell_Edge), (Cell_Edge*Col_Cnt-line_Width+x, y+Cell_Edge+i*Cell_Edge), line_Width)
            
    
    def draw_text(self, text, size, x, y):
        font_name = os.path.join("Assests/fonts", "font.ttf")
        font = pygame.font.Font(font_name, size)
        #繪製文字(文字, 平滑值, 文字顏色, 背景顏色)
        TEXT = font.render(text, True, self.WHITE)
        TEXT_rect = TEXT.get_rect()
        TEXT_rect.centerx = x
        TEXT_rect.centery = y
        self.screen.blit(TEXT, TEXT_rect)
        # pygame.display.update()
        
    def GameOver(self, x, y):
        img = pygame.image.load(os.path.join("Assests/imgs", "level_1.jpg")).convert()
        gameover_img = pygame.transform.scale(img, (200, 200))
        self.screen.blit(gameover_img, (x, y))
        self.draw_text("GAME OVER", 72, x+100, y+260)
        self.ScreenState = self.Button(("Go Back", 1400, 600, 100, 50, 0))
        if self.ScreenState == 0:
            return self.ScreenState
        else:
            return 5
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
            # self.screen.fill(self.WHITE)
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            # hover 狀態切換顏色
            for button in buttons:
                
                text, x, y, width, height, ScreenState, *optional = button
                color = optional[0] if len(optional) > 0 else default_color
                hover_color = optional[1] if len(optional) > 1 else default_hover_color
                txt_color = optional[2] if len(optional) > 2 else default_txt_color
                button_rect = pygame.Rect(x, y, width, height)
                text = font.render(text, True, txt_color)
                
                if button_rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    pygame.draw.rect(self.screen, hover_color, button_rect)
                    if click[0]:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        self.screen.fill(self.WHITE)
                        pygame.display.update()
                        return ScreenState
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    pygame.draw.rect(self.screen, color, button_rect)

                # 畫上文字（置中）
                text_rect = text.get_rect(center=button_rect.center)
                self.screen.blit(text, text_rect)   
            
            
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
