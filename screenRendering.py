import pygame

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
        running = True
        button1_rect = pygame.Rect(150, 120, 100, 50)
        button2_rect = pygame.Rect(150, 480, 100, 50)
        button_color = (0, 128, 255)
        button_hover_color = (0, 200, 255)
        text_color = (255, 255, 255)
        font = pygame.font.SysFont(None, 36)
        text1 = font.render("Single", True, text_color)
        text2 = font.render("Double", True, text_color)
        while running:
            self.screen.fill(self.WHITE)
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            # hover 狀態切換顏色
            if button1_rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                pygame.draw.rect(self.screen, button_hover_color, button1_rect)
                if click[0]:
                    print("single mode")
                    self.ScreenState = 1
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.screen.fill(self.WHITE)
                    pygame.display.update()
                    return self.ScreenState
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                pygame.draw.rect(self.screen, button_color, button1_rect)

            if button2_rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                pygame.draw.rect(self.screen, button_hover_color, button2_rect)
                if click[0]:
                    print("Double mode")
                    self.ScreenState = 2
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.screen.fill(self.WHITE)
                    pygame.display.update()
                    return self.ScreenState
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                pygame.draw.rect(self.screen, button_color, button2_rect)
            
            # 畫上文字（置中）
            text1_rect = text1.get_rect(center=button1_rect.center)
            self.screen.blit(text1, text1_rect)
            
            text2_rect = text2.get_rect(center=button2_rect.center)
            self.screen.blit(text2, text2_rect)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def SingleMode_Start(self):
        running = True
        button_rect = pygame.Rect(300, 150, 100, 50)
        button_color = (0, 128, 255)
        button_hover_color = (0, 200, 255)
        text_color = (255, 255, 255)
        font = pygame.font.SysFont(None, 36)
        text = font.render("Start", True, text_color)

        while running:
            self.screen.fill(self.WHITE)
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            # hover 狀態切換顏色
            if button_rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                pygame.draw.rect(self.screen, button_hover_color, button_rect)
                if click[0]:
                    print("single mode Start")
                    self.ScreenState = 3
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.screen.fill(self.WHITE)
                    pygame.display.update()
                    return self.ScreenState
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                pygame.draw.rect(self.screen, button_color, button_rect)

            # 畫上文字（置中）
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)   
            
            #遊戲畫面顯示
            player_Y = 50
            player1_X = 600
            self.GameCell(player1_X,player_Y,30,2,20,10)
            
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
    def DoubleMode_Start(self):
        running = True
        button_rect = pygame.Rect(700, 150, 100, 50)
        button_color = (0, 128, 255)
        button_hover_color = (0, 200, 255)
        text_color = (255, 255, 255)
        font = pygame.font.SysFont(None, 36)
        text = font.render("Start", True, text_color)

        while running:
            self.screen.fill(self.WHITE)
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            # hover 狀態切換顏色
            if button_rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                pygame.draw.rect(self.screen, button_hover_color, button_rect)
                if click[0]:
                    print("Double mode Start")
                    self.ScreenState = 4
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.screen.fill(self.WHITE)
                    pygame.display.update()
                    return self.ScreenState
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                pygame.draw.rect(self.screen, button_color, button_rect)

            # 畫上文字（置中）
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)   
            
            #遊戲畫面顯示
            player_Y = 50
            player1_X = 100
            player2_X = self.WIDTH-self.BAR_WIDTH-player1_X
            self.GameCell(player1_X,player_Y,30,2,20,10)
            self.GameCell(player2_X,player_Y,30,2,20,10)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
    
    def GameCell(self, x, y, Cell_Edge, line_Width, Row_Cnt, Col_Cnt):
        rect = pygame.Rect(x, y, self.BAR_WIDTH, self.BAR_HEIGHT)
        pygame.draw.rect(self.screen, self.LIGHT_GRAY, rect, line_Width)
        for i in range(Col_Cnt-1):
            pygame.draw.line(self.screen, self.LIGHT_GRAY, (x+(i+1)*Cell_Edge, y), (x+(i+1)*Cell_Edge, Cell_Edge*Row_Cnt-line_Width+y), line_Width)
        for i in range(Row_Cnt-1):
            pygame.draw.line(self.screen, self.LIGHT_GRAY, (x, y+Cell_Edge+i*Cell_Edge), (Cell_Edge*Col_Cnt-line_Width+x, y+Cell_Edge+i*Cell_Edge), line_Width)