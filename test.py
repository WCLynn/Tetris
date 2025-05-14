import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
font = pygame.font.SysFont(None, 36)

# 按鈕參數
button_rect = pygame.Rect(150, 120, 100, 50)
button_color = (0, 128, 255)
button_hover_color = (0, 200, 255)
text_color = (255, 255, 255)
text = font.render("點我", True, text_color)

running = True
while running:
    screen.fill((30, 30, 30))  # 背景色

    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # 畫按鈕（偵測滑鼠懸停改變顏色）
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, button_hover_color, button_rect)
        if click[0]:  # 左鍵點擊
            print("按鈕被點到了！")
    else:
        pygame.draw.rect(screen, button_color, button_rect)

    # 畫文字（置中）
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    # 處理事件關閉
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
